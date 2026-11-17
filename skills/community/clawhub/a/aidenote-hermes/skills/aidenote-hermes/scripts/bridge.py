#!/usr/bin/env python3
"""Install and inspect the verified AideNote local connection suite."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any
from urllib import error, request


GUIDE_URL = "https://www.aidenote.cn/mobile/workbuddy-skill-guide.html"
PAIRING_BASE = "https://api.aidenote.cn/agent-pair"
PAIRING_STATE_NAME = "aidenote-pairing.json"
EXPECTED_TUNNEL_VERSION = "3.2.6"
INSTALLERS = {
    "Darwin": {
        "url": f"https://cdn.aidenote.cn/tunnel/releases/{EXPECTED_TUNNEL_VERSION}/install-macos.sh",
        "sha256": "5afb27d2640b73689217775989253c0cdea05c4f35ea0ee9f86bb4c0551070cd",
        "suffix": ".sh",
    },
    "Windows": {
        "url": f"https://cdn.aidenote.cn/tunnel/releases/{EXPECTED_TUNNEL_VERSION}/install-windows.ps1",
        "sha256": "5a5a3ecee34e3dce6d2248744bcac854296ed0f4c3afab0f3a344c9f36d908f6",
        "suffix": ".ps1",
    },
}
MAX_INSTALLER_BYTES = 1_000_000


class BridgeError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def emit(value: Any, *, stream: Any = sys.stdout) -> None:
    json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
    stream.write("\n")


def hermes_home() -> Path:
    configured = os.environ.get("HERMES_HOME", "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".hermes"


def load_api_key() -> str:
    credentials_path = hermes_home() / "aidenote-credentials.json"
    if not credentials_path.is_file():
        raise BridgeError(
            "missing_credentials",
            "AideNote credentials are not configured. Run scripts/configure.py locally first.",
        )
    if os.name != "nt" and stat.S_IMODE(credentials_path.stat().st_mode) & 0o077:
        raise BridgeError(
            "insecure_credentials",
            "AideNote credentials must be readable only by the current user.",
        )
    try:
        credentials = json.loads(credentials_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BridgeError("invalid_credentials", "AideNote credentials could not be read.") from exc
    api_key = credentials.get("apiKey") if isinstance(credentials, dict) else None
    if not isinstance(api_key, str) or not api_key.strip():
        raise BridgeError("invalid_credentials", "AideNote credentials do not contain an API Key.")
    return api_key.strip()


def pairing_state_path() -> Path:
    return hermes_home() / PAIRING_STATE_NAME


def read_private_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def write_private_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        path.parent.chmod(0o700)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".aidenote-", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        if os.name != "nt":
            temporary_path.chmod(0o600)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def request_pairing(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    encoded = json.dumps(payload).encode("utf-8")
    req = request.Request(
        PAIRING_BASE + path,
        data=encoded,
        method="POST",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            decoded = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        try:
            decoded_error = json.loads(exc.read().decode("utf-8"))
            message = str(decoded_error.get("message") or "Pairing request was rejected.")
            code = str(decoded_error.get("code") or "pairing_failed")
        except (OSError, json.JSONDecodeError, AttributeError):
            message = f"Pairing request failed (HTTP {exc.code})."
            code = "pairing_failed"
        raise BridgeError(code, message) from exc
    except (error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise BridgeError("pairing_network_error", "Could not reach the AideNote pairing service.") from exc
    if not isinstance(decoded, dict):
        raise BridgeError("pairing_invalid_response", "The pairing service returned an invalid response.")
    return decoded


def pairing_public_state() -> dict[str, Any] | None:
    state = read_private_json(pairing_state_path())
    if not state:
        return None
    expires_at = int(state.get("expiresAt") or 0)
    return {
        "status": str(state.get("status") or "unknown"),
        "code": str(state.get("code") or ""),
        "expiresAt": expires_at,
        "expired": bool(expires_at and expires_at <= int(time.time())),
        "message": str(state.get("message") or ""),
    }


def port_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def read_bridge_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def bridge_status() -> dict[str, Any]:
    system = platform.system()
    home = Path.home()
    config_file = home / ".aidenote" / "openclaw-tunnel.json"
    config = read_bridge_config(config_file)
    if system == "Darwin":
        install_dir = home / "Library" / "Application Support" / "AideNote" / "OpenClawBridge"
        tunnel_binary = install_dir / "aide-note-tunnel"
        workbuddy_binary = install_dir / "aidenote-workbuddy-bridge"
        tunnel_service = home / "Library" / "LaunchAgents" / "cn.aidenote.openclaw-tunnel.plist"
        workbuddy_service = home / "Library" / "LaunchAgents" / "cn.aidenote.workbuddy-bridge.plist"
        hermes_service = home / "Library" / "LaunchAgents" / "ai.hermes.gateway.plist"
    elif system == "Windows":
        install_dir = home / "AppData" / "Local" / "AideNote" / "OpenClawBridge"
        tunnel_binary = install_dir / "aide-note-tunnel.exe"
        workbuddy_binary = install_dir / "aidenote-workbuddy-bridge.exe"
        tunnel_service = tunnel_binary
        workbuddy_service = workbuddy_binary
        hermes_service = hermes_home() / ".env"
    else:
        install_dir = Path()
        tunnel_binary = Path()
        workbuddy_binary = Path()
        tunnel_service = Path()
        workbuddy_service = Path()
        hermes_service = Path()
    release_info = read_bridge_config(install_dir / "release.json")
    installed_version = str(release_info.get("version") or "").strip()
    up_to_date = installed_version == EXPECTED_TUNNEL_VERSION
    files_installed = config_file.is_file() and tunnel_binary.is_file() and tunnel_service.is_file()
    hermes_token_configured = bool(str(config.get("hermesToken") or "").strip())
    hermes_reachable = port_open(8642)
    result = {
        "ok": files_installed and up_to_date and hermes_token_configured and hermes_reachable,
        "operation": "bridge-status",
        "platform": system,
        "supportedInstaller": system in INSTALLERS,
        "installed": files_installed,
        "installedVersion": installed_version,
        "expectedVersion": EXPECTED_TUNNEL_VERSION,
        "upToDate": up_to_date,
        "configPresent": config_file.is_file(),
        "installDirectoryPresent": install_dir.is_dir(),
        "tunnelBinaryPresent": tunnel_binary.is_file(),
        "tunnelStartupConfigured": tunnel_service.is_file(),
        "workBuddyBridgeBinaryPresent": workbuddy_binary.is_file(),
        "workBuddyStartupConfigured": workbuddy_service.is_file(),
        "hermesTokenConfigured": hermes_token_configured,
        "hermesStartupConfigured": hermes_service.is_file(),
        "ports": {
            "openclaw": {"port": 18789, "reachable": port_open(18789)},
            "hermes": {"port": 8642, "reachable": hermes_reachable},
            "workbuddy": {"port": 49985, "reachable": port_open(49985)},
            "workbuddyBridge": {"port": 55374, "reachable": port_open(55374)},
        },
        "installGuide": GUIDE_URL,
    }
    pairing = pairing_public_state()
    if pairing is not None:
        result["pairing"] = pairing
    return result


def worker_is_running(state: dict[str, Any]) -> bool:
    try:
        pid = int(state.get("workerPid") or 0)
        if pid <= 0:
            return False
        os.kill(pid, 0)
        return True
    except (OSError, TypeError, ValueError):
        return False


def spawn_pairing_worker(state: dict[str, Any]) -> None:
    child_environment = {
        "HOME": str(Path.home()),
        "PATH": os.pathsep.join(
            [
                str(Path.home() / ".local" / "bin"),
                str(Path.home() / ".hermes" / "bin"),
                "/opt/homebrew/bin",
                "/usr/local/bin",
                "/usr/bin",
                "/bin",
            ]
        ),
    }
    configured_home = os.environ.get("HERMES_HOME", "").strip()
    if configured_home:
        child_environment["HERMES_HOME"] = configured_home
    if os.name == "nt":
        optional_windows_environment = {
            "USERPROFILE": os.environ.get("USERPROFILE", ""),
            "LOCALAPPDATA": os.environ.get("LOCALAPPDATA", ""),
            "SystemRoot": os.environ.get("SystemRoot", ""),
            "TEMP": os.environ.get("TEMP", ""),
            "TMP": os.environ.get("TMP", ""),
        }
        for name, value in optional_windows_environment.items():
            if value:
                child_environment[name] = value
    popen_options: dict[str, Any] = {
        "env": child_environment,
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "close_fds": True,
    }
    if os.name == "nt":
        popen_options["creationflags"] = 0x00000008 | 0x00000200
    else:
        popen_options["start_new_session"] = True
    process = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "pair-worker"],
        **popen_options,
    )
    state["workerPid"] = process.pid
    write_private_json(pairing_state_path(), state)


def start_pairing_install() -> dict[str, Any]:
    state = read_private_json(pairing_state_path())
    now = int(time.time())
    reusable = (
        state.get("status") == "pending"
        and int(state.get("expiresAt") or 0) > now + 15
        and state.get("pairId")
        and state.get("secret")
        and state.get("code")
    )
    if not reusable:
        started = request_pairing("/start", {})
        expires_in = int(started.get("expiresIn") or 600)
        state = {
            "status": "pending",
            "pairId": str(started.get("pairId") or ""),
            "secret": str(started.get("secret") or ""),
            "code": str(started.get("code") or ""),
            "expiresAt": now + expires_in,
            "message": "Waiting for approval in the AideNote app.",
        }
        if not state["pairId"] or not state["secret"] or len(state["code"]) != 8:
            raise BridgeError("pairing_invalid_response", "The pairing service did not return a valid code.")
        write_private_json(pairing_state_path(), state)
    if not worker_is_running(state):
        spawn_pairing_worker(state)
    return {
        "ok": True,
        "operation": "bridge-pairing",
        "status": "pairing_required",
        "pairingCode": state["code"],
        "expiresAt": state["expiresAt"],
        "instructions": "Open AideNote > Add Assistant > Hermes, enter this code, and confirm the connection.",
    }


def write_pairing_credentials(api_key: str) -> None:
    write_private_json(
        hermes_home() / "aidenote-credentials.json",
        {"apiBase": "https://api.aidenote.cn", "apiKey": api_key},
    )


def update_pairing_state(state: dict[str, Any], status: str, message: str) -> None:
    state["status"] = status
    state["message"] = message
    state["updatedAt"] = int(time.time())
    state.pop("workerPid", None)
    write_private_json(pairing_state_path(), state)


def run_pairing_worker() -> int:
    state = read_private_json(pairing_state_path())
    pair_id = str(state.get("pairId") or "")
    secret = str(state.get("secret") or "")
    expires_at = int(state.get("expiresAt") or 0)
    if not pair_id or not secret or expires_at <= int(time.time()):
        return 2
    approved = False
    try:
        while int(time.time()) < expires_at:
            result = request_pairing("/status", {"pairId": pair_id, "secret": secret})
            if result.get("status") == "approved":
                api_key = str(result.get("apiKey") or "").strip()
                if not api_key:
                    raise BridgeError("pairing_invalid_response", "Pairing approval did not include credentials.")
                approved = True
                write_pairing_credentials(api_key)
                state["status"] = "installing"
                state["message"] = "Pairing approved; installing the local connection suite."
                write_private_json(pairing_state_path(), state)
                install_bridge()
                update_pairing_state(state, "installed", "AideNote connection installed successfully.")
                return 0
            time.sleep(3)
        update_pairing_state(state, "expired", "The pairing code expired. Start installation again.")
        return 2
    except BridgeError as exc:
        update_pairing_state(state, "failed", exc.message)
        return 2
    finally:
        if approved:
            try:
                request_pairing("/complete", {"pairId": pair_id, "secret": secret})
            except BridgeError:
                pass


def download_verified_installer(system: str) -> Path:
    metadata = INSTALLERS[system]
    req = request.Request(
        str(metadata["url"]),
        headers={"User-Agent": "AideNote-Hermes-Skill/1.1"},
        method="GET",
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            final_url = response.geturl()
            if not final_url.lower().startswith("https://"):
                raise BridgeError("insecure_download", "The installer redirected to a non-HTTPS URL.")
            content = response.read(MAX_INSTALLER_BYTES + 1)
    except BridgeError:
        raise
    except error.HTTPError as exc:
        raise BridgeError("download_failed", f"Installer download failed (HTTP {exc.code}).") from exc
    except (error.URLError, TimeoutError, OSError) as exc:
        raise BridgeError("download_failed", "Could not download the official AideNote installer.") from exc
    if len(content) > MAX_INSTALLER_BYTES:
        raise BridgeError("invalid_installer", "The downloaded installer is unexpectedly large.")
    actual_hash = hashlib.sha256(content).hexdigest()
    if actual_hash != metadata["sha256"]:
        raise BridgeError("checksum_mismatch", "The installer failed SHA-256 verification.")
    descriptor, name = tempfile.mkstemp(prefix="aidenote-installer-", suffix=str(metadata["suffix"]))
    path = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        if os.name != "nt":
            path.chmod(0o700)
        return path
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def safe_output(stdout: str, stderr: str) -> str:
    lines = []
    for raw_line in (stdout + "\n" + stderr).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("% Total") or line.startswith("Dload  Upload"):
            continue
        lines.append(line)
    return "\n".join(lines[-20:])[-4000:]


def install_bridge() -> dict[str, Any]:
    system = platform.system()
    if system not in INSTALLERS:
        raise BridgeError("unsupported_platform", "Automatic installation supports macOS and Windows only.")
    api_key = load_api_key()
    installer = download_verified_installer(system)
    if system == "Darwin":
        path_value = os.pathsep.join(
            str(path)
            for path in (
                Path.home() / ".local" / "bin",
                Path.home() / ".hermes" / "bin",
                Path("/opt/homebrew/bin"),
                Path("/usr/local/bin"),
                Path("/usr/bin"),
                Path("/bin"),
                Path("/usr/sbin"),
                Path("/sbin"),
            )
        )
    else:
        system_root = Path(os.environ.get("SystemRoot", "C:\\Windows"))
        path_value = os.pathsep.join(
            str(path)
            for path in (
                system_root / "System32" / "WindowsPowerShell" / "v1.0",
                system_root / "System32",
                system_root,
                Path.home() / ".local" / "bin",
                Path.home() / ".hermes" / "bin",
            )
        )
    installer_environment = {
        "AIDE_NOTE_API_KEY": api_key,
        "AIDE_NOTE_TUNNEL_BASE_URL": f"https://cdn.aidenote.cn/tunnel/releases/{EXPECTED_TUNNEL_VERSION}",
        "AIDE_NOTE_REPLACE_API_KEY": "1",
        "AIDE_NOTE_RESET_DEVICE_ID": "1",
        "HOME": str(Path.home()),
        "PATH": path_value,
    }
    optional_environment = {
        "USER": os.environ.get("USER", ""),
        "LOGNAME": os.environ.get("LOGNAME", ""),
        "LOCALAPPDATA": os.environ.get("LOCALAPPDATA", ""),
        "USERPROFILE": os.environ.get("USERPROFILE", ""),
        "PROCESSOR_ARCHITECTURE": os.environ.get("PROCESSOR_ARCHITECTURE", ""),
        "SystemRoot": os.environ.get("SystemRoot", ""),
        "TEMP": os.environ.get("TEMP", ""),
        "TMP": os.environ.get("TMP", ""),
    }
    for name, value in optional_environment.items():
        if value:
            installer_environment[name] = value
    if system == "Darwin":
        command = ["/bin/bash", str(installer)]
    else:
        powershell = shutil.which("pwsh", path=path_value) or shutil.which("powershell", path=path_value)
        if not powershell:
            installer.unlink(missing_ok=True)
            raise BridgeError("powershell_missing", "PowerShell is required to install the AideNote bridge.")
        command = [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(installer)]
    try:
        completed = subprocess.run(
            command,
            env=installer_environment,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError("installer_timeout", "The AideNote installer did not finish within 10 minutes.") from exc
    finally:
        installer.unlink(missing_ok=True)
    output = safe_output(completed.stdout, completed.stderr)
    if completed.returncode != 0:
        raise BridgeError(
            "installer_failed",
            f"The AideNote installer failed with exit code {completed.returncode}. {output}",
        )
    status = bridge_status()
    if not status["ok"]:
        raise BridgeError("verification_failed", "Installation finished, but the Hermes bridge is not healthy.")
    return {
        "ok": True,
        "operation": "bridge-install",
        "installed": True,
        "verified": True,
        "status": status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Install or inspect the AideNote local connection suite")
    parser.add_argument("command", choices=["status", "install", "pair-worker"])
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirm installation of verified local services and login/startup entries",
    )
    args = parser.parse_args()
    try:
        if args.command == "pair-worker":
            return run_pairing_worker()
        if args.command == "status":
            emit(bridge_status())
            return 0
        if not args.confirm:
            raise BridgeError(
                "confirmation_required",
                "Installation changes local services. Run install --confirm only after the user explicitly asks to install.",
            )
        try:
            load_api_key()
        except BridgeError as exc:
            if exc.code != "missing_credentials":
                raise
            emit(start_pairing_install())
            return 0
        emit(install_bridge())
        return 0
    except BridgeError as exc:
        emit({"ok": False, "error": exc.code, "message": exc.message}, stream=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
