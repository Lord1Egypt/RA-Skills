#!/usr/bin/env python3
"""Persistent session daemon for ChatGPT Web."""

from __future__ import annotations

import argparse
import atexit
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

from patchright.sync_api import sync_playwright

try:
    import fcntl  # type: ignore
except ImportError:
    fcntl = None

sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_session import ChatGPTBrowserSession
from browser_utils import BrowserFactory
from config import DATA_DIR, RESPONSE_TIMEOUT_SECONDS, SESSION_RUNTIME_DIR, SESSIONS_FILE
from errors import ChatGPTSkillError, result_from_exception
from storage import load_json_file, save_json_file, utcnow_iso


SESSIONS_LOCK_FILE = DATA_DIR / "sessions.lock"
SOCKET_FILE = SESSION_RUNTIME_DIR / "session_manager.sock"
PID_FILE = SESSION_RUNTIME_DIR / "session_manager.pid"
DEFAULT_IDLE_TIMEOUT_SECONDS = int(os.getenv("CHATGPT_SESSION_IDLE_TIMEOUT", "1800"))
DEFAULT_CLIENT_TIMEOUT_SECONDS = max(RESPONSE_TIMEOUT_SECONDS + 60, 240)
DAEMON_START_TIMEOUT_SECONDS = 12
ACTIVE_STATUSES = {"active", "busy"}


class SessionManagerError(RuntimeError):
    def __init__(self, message: str, *, error_code: str = "session_manager_error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_result(self, **extra: Any) -> Dict[str, Any]:
        payload = {
            "status": "error",
            "error_code": self.error_code,
            "error": self.message,
        }
        payload.update(self.details)
        payload.update(extra)
        return payload


@contextmanager
def file_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+", encoding="utf-8") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class SessionMetadataStore:
    def __init__(self, path: Path = SESSIONS_FILE):
        self.path = path
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _default(self) -> Dict[str, Any]:
        return {
            "version": 1,
            "updated_at": utcnow_iso(),
            "daemon": {
                "pid": None,
                "started_at": None,
                "socket": str(SOCKET_FILE),
                "idle_timeout_seconds": DEFAULT_IDLE_TIMEOUT_SECONDS,
                "status": "stopped",
            },
            "sessions": {},
        }

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return self._default()
        with file_lock(SESSIONS_LOCK_FILE):
            payload = load_json_file(self.path, self._default())
        if not isinstance(payload, dict):
            return self._default()
        payload.setdefault("version", 1)
        payload.setdefault("updated_at", utcnow_iso())
        payload.setdefault("daemon", self._default()["daemon"])
        payload.setdefault("sessions", {})
        return payload

    def save(self, payload: Dict[str, Any]):
        payload["updated_at"] = utcnow_iso()
        with file_lock(SESSIONS_LOCK_FILE):
            save_json_file(self.path, payload)

    def set_daemon(self, *, pid: Optional[int], started_at: Optional[str], status: str, idle_timeout_seconds: int):
        payload = self.load()
        payload["daemon"] = {
            "pid": pid,
            "started_at": started_at,
            "socket": str(SOCKET_FILE),
            "idle_timeout_seconds": idle_timeout_seconds,
            "status": status,
        }
        self.save(payload)

    def upsert_session(self, record: Dict[str, Any]):
        payload = self.load()
        payload["sessions"][record["session_id"]] = record
        self.save(payload)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.load().get("sessions", {}).get(session_id)

    def list_sessions(self) -> List[Dict[str, Any]]:
        sessions = list(self.load().get("sessions", {}).values())
        sessions.sort(key=lambda item: item.get("last_activity", ""), reverse=True)
        return sessions

    def update_session(self, session_id: str, **updates):
        payload = self.load()
        record = payload.get("sessions", {}).get(session_id)
        if not record:
            return None
        record.update(updates)
        payload["sessions"][session_id] = record
        self.save(payload)
        return record

    def mark_runtime_sessions_orphaned(self):
        payload = self.load()
        changed = 0
        for record in payload.get("sessions", {}).values():
            if record.get("status") in ACTIVE_STATUSES:
                record["status"] = "orphaned"
                record["last_error"] = "session daemon is not running anymore"
                changed += 1
        if changed:
            payload["daemon"]["pid"] = None
            payload["daemon"]["status"] = "stopped"
            self.save(payload)
        return changed


class SessionManagerClient:
    def __init__(self, socket_path: Path = SOCKET_FILE):
        self.socket_path = socket_path
        self.store = SessionMetadataStore()

    def _cleanup_stale_runtime_files(self):
        for path in (SOCKET_FILE, PID_FILE):
            if path.exists():
                try:
                    path.unlink()
                except OSError:
                    pass

    def _send(self, request: Dict[str, Any], timeout_seconds: int) -> Dict[str, Any]:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout_seconds)
            sock.connect(str(self.socket_path))
            sock.sendall((json.dumps(request, ensure_ascii=False) + "\n").encode("utf-8"))
            sock.shutdown(socket.SHUT_WR)
            chunks: List[bytes] = []
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                chunks.append(chunk)
        raw = b"".join(chunks).decode("utf-8").strip()
        if not raw:
            raise SessionManagerError("Empty response from session daemon")
        return json.loads(raw)

    def is_daemon_running(self) -> bool:
        if not self.socket_path.exists():
            return False
        try:
            self._send({"command": "ping"}, timeout_seconds=5)
            return True
        except Exception:
            return False

    def reconcile_runtime_state(self):
        if self.is_daemon_running():
            return
        self._cleanup_stale_runtime_files()
        self.store.mark_runtime_sessions_orphaned()

    def ensure_daemon(self):
        if self.is_daemon_running():
            return
        self._cleanup_stale_runtime_files()
        cmd = [sys.executable, str(Path(__file__).resolve()), "_serve"]
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            cwd=str(Path(__file__).parent.parent),
        )
        deadline = time.time() + DAEMON_START_TIMEOUT_SECONDS
        while time.time() < deadline:
            if self.is_daemon_running():
                return
            time.sleep(0.2)
        raise SessionManagerError("Failed to start session daemon")

    def request(self, command: str, *, auto_start: bool = False, timeout_seconds: Optional[int] = None, **payload) -> Dict[str, Any]:
        if auto_start:
            self.ensure_daemon()
        else:
            self.reconcile_runtime_state()
            if not self.is_daemon_running():
                raise SessionManagerError("Session daemon is not running")
        response = self._send({"command": command, **payload}, timeout_seconds or DEFAULT_CLIENT_TIMEOUT_SECONDS)
        if not response.get("ok"):
            raise SessionManagerError(
                response.get("error", "Unknown session manager error"),
                error_code=response.get("error_code", "session_manager_error"),
                details=response.get("details") if isinstance(response.get("details"), dict) else None,
            )
        return response["result"]


class ChatGPTSessionDaemon:
    def __init__(self, idle_timeout_seconds: int = DEFAULT_IDLE_TIMEOUT_SECONDS):
        self.idle_timeout_seconds = idle_timeout_seconds
        self.store = SessionMetadataStore()
        self.auth = AuthManager()
        self.playwright = None
        self.context = None
        self.sessions: Dict[str, ChatGPTBrowserSession] = {}
        self.running = True
        self.started_at = utcnow_iso()
        self.pid = os.getpid()

    def _install_signal_handlers(self):
        def handle_signal(_signum, _frame):
            self.running = False

        for signum in (signal.SIGTERM, signal.SIGINT):
            try:
                signal.signal(signum, handle_signal)
            except Exception:
                pass

    def _cleanup_runtime_files(self):
        for path in (SOCKET_FILE, PID_FILE):
            if path.exists():
                try:
                    path.unlink()
                except OSError:
                    pass

    def _ensure_browser(self):
        if self.context is not None:
            return
        validation = self.auth.validate_auth(headless=BrowserFactory.recommended_headless(default=True))
        if not validation.get("authenticated"):
            raise SessionManagerError("ChatGPT authentication is missing. Run: python scripts/run.py auth_manager.py setup")
        self.playwright = sync_playwright().start()
        self.context = BrowserFactory.launch_persistent_context(
            self.playwright,
            headless=BrowserFactory.recommended_headless(default=True),
        )

    def _build_metadata(self, session: ChatGPTBrowserSession, *, status: str, last_error: Optional[str] = None) -> Dict[str, Any]:
        return {
            "session_id": session.id,
            "conversation_id": session.conversation_id,
            "conversation_id_source": getattr(session, "conversation_id_source", None),
            "final_url": session.page.url if session.page else None,
            "created_at": getattr(session, "created_at_iso", None) or utcnow_iso(),
            "last_activity": utcnow_iso(),
            "message_count": session.message_count,
            "status": status,
            "last_error": last_error,
            "daemon_pid": self.pid,
            "idle_timeout_seconds": self.idle_timeout_seconds,
        }

    def run(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SESSION_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        self.store.mark_runtime_sessions_orphaned()
        self.store.set_daemon(
            pid=self.pid,
            started_at=self.started_at,
            status="running",
            idle_timeout_seconds=self.idle_timeout_seconds,
        )
        self._install_signal_handlers()
        atexit.register(self._cleanup_runtime_files)
        if SOCKET_FILE.exists():
            SOCKET_FILE.unlink()
        with open(PID_FILE, "w", encoding="utf-8") as handle:
            handle.write(str(self.pid))

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
            server.bind(str(SOCKET_FILE))
            os.chmod(SOCKET_FILE, 0o600)
            server.listen(16)
            server.settimeout(1.0)
            while self.running:
                try:
                    conn, _ = server.accept()
                except socket.timeout:
                    self.gc_sessions()
                    continue
                with conn:
                    response = self._handle_connection(conn)
                    conn.sendall((json.dumps(response, ensure_ascii=False) + "\n").encode("utf-8"))

        self.shutdown()

    def _handle_connection(self, conn: socket.socket) -> Dict[str, Any]:
        chunks: List[bytes] = []
        while True:
            chunk = conn.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
        raw = b"".join(chunks).decode("utf-8").strip()
        if not raw:
            return {"ok": False, "error": "Empty request"}
        try:
            request = json.loads(raw)
            result = self._dispatch(request)
            return {"ok": True, "result": result}
        except ChatGPTSkillError as error:
            return {"ok": False, "error": error.message, "error_code": error.code, "details": error.details}
        except SessionManagerError as error:
            return {"ok": False, "error": error.message, "error_code": error.error_code, "details": error.details}
        except Exception as error:
            return {"ok": False, "error": str(error), "error_code": "unexpected_error"}

    def _dispatch(self, request: Dict[str, Any]) -> Dict[str, Any]:
        command = request.get("command")
        if command == "ping":
            return {"status": "ok", "pid": self.pid, "session_count": len(self.sessions)}
        if command == "create":
            return self.create_session(request.get("conversation_id"))
        if command == "ask":
            return self.ask_session(
                request.get("session_id"),
                request.get("question"),
                model=request.get("model"),
                extended_thinking=bool(request.get("extended_thinking")),
                new_chat=bool(request.get("new_chat")),
                proof_screenshot=bool(request.get("proof_screenshot")),
            )
        if command == "list":
            return self.list_sessions()
        if command == "info":
            return self.info_session(request.get("session_id"))
        if command == "reset":
            return self.reset_session(request.get("session_id"))
        if command == "close":
            return self.close_session(request.get("session_id"), reason="closed")
        if command == "gc":
            return self.gc_sessions()
        raise SessionManagerError(f"Unsupported command: {command}")

    def _get_live_session(self, session_id: Optional[str]) -> ChatGPTBrowserSession:
        if not session_id:
            raise SessionManagerError("Missing session_id")
        session = self.sessions.get(session_id)
        if session is None:
            record = self.store.get_session(session_id)
            if record and record.get("status") == "orphaned":
                raise SessionManagerError("Session exists in metadata but its live browser process is gone")
            raise SessionManagerError(f"Session not found: {session_id}")
        return session

    def create_session(self, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        self.gc_sessions()
        self._ensure_browser()
        session_id = f"session-{uuid.uuid4().hex[:12]}"
        session = ChatGPTBrowserSession(session_id=session_id, context=self.context, conversation_id=conversation_id)
        session.created_at_iso = utcnow_iso()
        if not conversation_id:
            session.new_chat()
        self.sessions[session_id] = session
        metadata = self._build_metadata(session, status="active")
        self.store.upsert_session(metadata)
        return metadata

    def ask_session(
        self,
        session_id: Optional[str],
        question: Optional[str],
        *,
        model: Optional[str] = None,
        extended_thinking: bool = False,
        new_chat: bool = False,
        proof_screenshot: bool = False,
    ) -> Dict[str, Any]:
        if not question:
            raise SessionManagerError("Missing question")
        session = self._get_live_session(session_id)
        self.store.update_session(session.id, status="busy", last_error=None)
        try:
            payload = session.ask(
                question,
                model=model,
                extended_thinking=extended_thinking,
                new_chat=new_chat,
                proof_screenshot=proof_screenshot,
            )
        except ChatGPTSkillError as error:
            self.store.update_session(session.id, status="active", last_error=error.message, last_activity=utcnow_iso())
            raise
        except Exception as error:
            self.store.update_session(session.id, status="active", last_error=str(error), last_activity=utcnow_iso())
            raise SessionManagerError(str(error), error_code="unexpected_error") from error
        metadata = self._build_metadata(session, status="active")
        self.store.upsert_session(metadata)
        return {**metadata, **payload}

    def list_sessions(self) -> Dict[str, Any]:
        self.gc_sessions()
        records = []
        for record in self.store.list_sessions():
            item = dict(record)
            item["live"] = item.get("session_id") in self.sessions
            records.append(item)
        return {"status": "success", "count": len(records), "sessions": records}

    def info_session(self, session_id: Optional[str]) -> Dict[str, Any]:
        if not session_id:
            raise SessionManagerError("Missing session_id")
        record = self.store.get_session(session_id)
        if not record:
            raise SessionManagerError(f"Session not found: {session_id}")
        return {**record, "live": session_id in self.sessions}

    def reset_session(self, session_id: Optional[str]) -> Dict[str, Any]:
        session = self._get_live_session(session_id)
        payload = session.reset()
        metadata = self._build_metadata(session, status="active")
        self.store.upsert_session(metadata)
        return {**metadata, **payload}

    def close_session(self, session_id: Optional[str], *, reason: str) -> Dict[str, Any]:
        if not session_id:
            raise SessionManagerError("Missing session_id")
        session = self.sessions.pop(session_id, None)
        record = self.store.get_session(session_id)
        if session is None and record is None:
            raise SessionManagerError(f"Session not found: {session_id}")
        if session is not None:
            session.close()
            record = self._build_metadata(session, status=reason)
        else:
            record = dict(record)
            record["status"] = reason
        record["closed_at"] = utcnow_iso()
        self.store.upsert_session(record)
        return record

    def gc_sessions(self) -> Dict[str, Any]:
        expired = []
        for session_id, session in list(self.sessions.items()):
            if session.is_expired(self.idle_timeout_seconds):
                expired.append(session_id)
                self.close_session(session_id, reason="expired")
        return {
            "status": "success",
            "expired_count": len(expired),
            "expired_session_ids": expired,
            "remaining_live_sessions": len(self.sessions),
        }

    def shutdown(self):
        for session in list(self.sessions.values()):
            try:
                session.close()
            except Exception:
                pass
        self.sessions.clear()
        if self.context:
            try:
                self.context.close()
            except Exception:
                pass
            self.context = None
        if self.playwright:
            try:
                self.playwright.stop()
            except Exception:
                pass
            self.playwright = None
        self.store.set_daemon(pid=None, started_at=self.started_at, status="stopped", idle_timeout_seconds=self.idle_timeout_seconds)
        self._cleanup_runtime_files()


def print_json(payload: Dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status") == "success" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage persistent ChatGPT sessions")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--conversation-id")
    ask_parser = subparsers.add_parser("ask")
    ask_parser.add_argument("--session-id", required=True)
    ask_parser.add_argument("--question", required=True)
    ask_parser.add_argument("--model")
    ask_parser.add_argument("--extended-thinking", action="store_true")
    ask_parser.add_argument("--new-chat", action="store_true")
    ask_parser.add_argument("--proof-screenshot", action="store_true")
    subparsers.add_parser("list")
    info_parser = subparsers.add_parser("info")
    info_parser.add_argument("--session-id", required=True)
    reset_parser = subparsers.add_parser("reset")
    reset_parser.add_argument("--session-id", required=True)
    close_parser = subparsers.add_parser("close")
    close_parser.add_argument("--session-id", required=True)
    subparsers.add_parser("gc")
    subparsers.add_parser("_serve")

    args = parser.parse_args()

    if args.command == "_serve":
        daemon = ChatGPTSessionDaemon()
        daemon.run()
        return 0

    client = SessionManagerClient()
    client.reconcile_runtime_state()

    try:
        if args.command == "create":
            payload = {"status": "success", "result": client.request("create", auto_start=True, conversation_id=args.conversation_id)}
        elif args.command == "ask":
            payload = client.request(
                "ask",
                session_id=args.session_id,
                question=args.question,
                model=args.model,
                extended_thinking=args.extended_thinking,
                new_chat=args.new_chat,
                proof_screenshot=args.proof_screenshot,
            )
        elif args.command == "list":
            if client.is_daemon_running():
                payload = client.request("list")
            else:
                store = SessionMetadataStore()
                payload = {"status": "success", "count": len(store.list_sessions()), "sessions": [{**item, "live": False} for item in store.list_sessions()]}
        elif args.command == "info":
            if client.is_daemon_running():
                payload = {"status": "success", "session": client.request("info", session_id=args.session_id)}
            else:
                store = SessionMetadataStore()
                record = store.get_session(args.session_id)
                if not record:
                    raise SessionManagerError(f"Session not found: {args.session_id}")
                payload = {"status": "success", **record, "live": False}
        elif args.command == "reset":
            payload = {"status": "success", "result": client.request("reset", session_id=args.session_id)}
        elif args.command == "close":
            payload = {"status": "success", "result": client.request("close", session_id=args.session_id)}
        elif args.command == "gc":
            if client.is_daemon_running():
                payload = client.request("gc")
            else:
                payload = {"status": "success", "expired_count": 0, "expired_session_ids": [], "remaining_live_sessions": 0}
        else:
            parser.print_help()
            return 1
    except SessionManagerError as error:
        payload = error.to_result()
    except Exception as error:
        payload = result_from_exception(error)

    return print_json(payload)


if __name__ == "__main__":
    sys.exit(main())
