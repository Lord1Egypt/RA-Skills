#!/usr/bin/env python3
"""Repair hidden Codex Desktop history after local session migration.

The repair keeps all changes local to CODEX_HOME, creates backups, and avoids
secrets. It fixes the common failure mode where Codex Desktop's thread/list
filters migrated sessions because source/model_provider metadata does not match
the current desktop provider.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import queue
import shutil
import sqlite3
import stat
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def utc_iso_from_ms(value: int) -> str:
    return dt.datetime.fromtimestamp(value / 1000, tz=dt.timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_path(value: str | None) -> str | None:
    if not value:
        return value
    return value[4:] if value.startswith("\\\\?\\") else value


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    content = "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows)
    if content:
        content += "\n"
    path.write_text(content, encoding="utf-8")


def set_json_prop(obj: dict[str, Any], key: str, value: Any) -> None:
    obj[key] = value


def default_codex_home() -> Path:
    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return Path(env_home)
    return Path.home() / ".codex"


def ensure_writable(path: Path) -> None:
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWRITE)


def backup_state(home: Path, backup_dir: Path, dry_run: bool) -> None:
    if dry_run:
        return
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        ".codex-global-state.json",
        ".codex-global-state.json.bak",
        "session_index.jsonl",
        "history.jsonl",
    ):
        source = home / name
        if source.exists():
            shutil.copy2(source, backup_dir / name)

    db_path = home / "state_5.sqlite"
    if db_path.exists():
        con = sqlite3.connect(db_path)
        try:
            with sqlite3.connect(backup_dir / "state_5.sqlite") as dst:
                con.backup(dst)
        finally:
            con.close()


def fetch_threads(con: sqlite3.Connection, target: str) -> list[sqlite3.Row]:
    where = "" if target == "all" else "WHERE archived = 0"
    return list(
        con.execute(
            f"""
            SELECT id, rollout_path, cwd, title, updated_at, updated_at_ms,
                   created_at, created_at_ms, archived, archived_at
            FROM threads
            {where}
            ORDER BY COALESCE(updated_at_ms, updated_at * 1000) DESC, updated_at DESC
            """
        )
    )


def resolve_provider_and_source(
    con: sqlite3.Connection,
    provider: str,
    source: str,
) -> tuple[str, str]:
    if provider != "auto" and source != "auto":
        return provider, source

    latest = con.execute(
        """
        SELECT model_provider, source
          FROM threads
         WHERE archived = 0
         ORDER BY COALESCE(updated_at_ms, updated_at * 1000) DESC, updated_at DESC
         LIMIT 1
        """
    ).fetchone()

    if provider == "auto":
        provider = (latest["model_provider"] if latest else None) or "OpenAI"
    if source == "auto":
        source = (latest["source"] if latest else None) or "vscode"
    return provider, source


def repair_database(
    con: sqlite3.Connection,
    threads: list[sqlite3.Row],
    provider: str,
    source: str,
    thread_source: str,
    unarchive: bool,
    dry_run: bool,
) -> None:
    if dry_run:
        return
    for row in threads:
        created_at_ms = row["created_at_ms"] or (int(row["created_at"]) * 1000)
        updated_at_ms = row["updated_at_ms"] or (int(row["updated_at"]) * 1000)
        archived = 0 if unarchive else row["archived"]
        archived_at = None if unarchive else row["archived_at"]
        con.execute(
            """
            UPDATE threads
               SET cwd = ?,
                   rollout_path = ?,
                   source = ?,
                   thread_source = ?,
                   model_provider = ?,
                   created_at_ms = ?,
                   updated_at_ms = ?,
                   archived = ?,
                   archived_at = ?
             WHERE id = ?
            """,
            (
                normalize_path(row["cwd"]),
                normalize_path(row["rollout_path"]),
                source,
                thread_source,
                provider,
                created_at_ms,
                updated_at_ms,
                archived,
                archived_at,
                row["id"],
            ),
        )
    con.commit()


def patch_rollout_files(
    threads: list[sqlite3.Row],
    provider: str,
    source: str,
    thread_source: str,
    backup_dir: Path,
    dry_run: bool,
) -> tuple[int, int, int]:
    changed = 0
    skipped_locked = 0
    missing = 0
    rollout_backup_dir = backup_dir / "rollouts"

    for row in threads:
        raw_path = normalize_path(row["rollout_path"])
        if not raw_path:
            missing += 1
            continue
        path = Path(raw_path)
        if not path.exists():
            missing += 1
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            skipped_locked += 1
            continue

        if not lines:
            continue
        try:
            first = json.loads(lines[0])
        except json.JSONDecodeError:
            continue
        payload = first.get("payload")
        if first.get("type") != "session_meta" or not isinstance(payload, dict):
            continue

        before = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        set_json_prop(payload, "model_provider", provider)
        set_json_prop(payload, "source", source)
        set_json_prop(payload, "thread_source", thread_source)
        if payload.get("cwd"):
            set_json_prop(payload, "cwd", normalize_path(str(payload["cwd"])))
        after = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        if before == after:
            continue

        changed += 1
        if dry_run:
            continue
        rollout_backup_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{row['id']}-{path.name}"
        shutil.copy2(path, rollout_backup_dir / safe_name)
        lines[0] = json.dumps(first, ensure_ascii=False, separators=(",", ":"))
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return changed, skipped_locked, missing


def rebuild_history_files(home: Path, threads: list[sqlite3.Row], dry_run: bool) -> int:
    index_rows: list[dict[str, Any]] = []
    history_rows: list[dict[str, Any]] = []

    for row in threads:
        updated_ms = row["updated_at_ms"] or (int(row["updated_at"]) * 1000)
        title = row["title"] or ""
        index_rows.append(
            {
                "id": row["id"],
                "thread_name": title,
                "updated_at": utc_iso_from_ms(int(updated_ms)),
            }
        )
        history_rows.append(
            {
                "session_id": row["id"],
                "ts": int(updated_ms) // 1000,
                "text": title,
            }
        )

    if not dry_run:
        write_jsonl(home / "session_index.jsonl", index_rows)
        write_jsonl(home / "history.jsonl", history_rows)
    return len(index_rows)


def derive_root(cwd: str, documents: Path) -> str | None:
    path = normalize_path(cwd)
    if not path:
        return None

    lowered = path.lower()
    codex_docs = str(documents / "Codex")
    new_project = str(documents / "New project")
    if lowered.startswith(codex_docs.lower() + "\\") or lowered == codex_docs.lower():
        return codex_docs
    if lowered.startswith(new_project.lower() + "\\") or lowered == new_project.lower():
        return new_project
    if lowered.startswith("d:\\object\\"):
        parts = path.split("\\")
        if len(parts) >= 3:
            return "\\".join(parts[:3])
    if Path(path).exists():
        return path
    return None


def find_project_root(cwd: str, roots: list[str]) -> str | None:
    normalized = normalize_path(cwd) or ""
    candidates = []
    for root in roots:
        stripped = root.rstrip("\\")
        if normalized.lower() == stripped.lower() or normalized.lower().startswith((stripped + "\\").lower()):
            candidates.append(root)
    return max(candidates, key=len) if candidates else None


def build_project_roots(
    state: dict[str, Any],
    threads: list[sqlite3.Row],
    scan_parents: list[Path],
    keep_existing_roots: bool = False,
) -> list[str]:
    roots: list[str] = []

    def add(value: str | None) -> None:
        if value and value not in roots:
            roots.append(value)

    if keep_existing_roots:
        for value in state.get("electron-saved-workspace-roots", []) or []:
            add(normalize_path(str(value)))

    documents = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "Documents"
    for row in threads:
        add(derive_root(row["cwd"], documents))

    for parent in scan_parents:
        if parent.exists():
            for child in sorted(parent.iterdir(), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
                if child.is_dir() and "backup" not in child.name.lower() and "staging" not in child.name.lower():
                    add(str(child))

    return roots


def build_repaired_global_state(
    state: dict[str, Any],
    threads: list[sqlite3.Row],
    scan_parents: list[Path],
    keep_existing_roots: bool,
) -> dict[str, Any]:
    original_roots = [normalize_path(str(value)) for value in state.get("electron-saved-workspace-roots", []) or []]
    roots = build_project_roots(state, threads, scan_parents, keep_existing_roots=keep_existing_roots)
    pruned_roots = [root for root in original_roots if root and root not in roots]

    hints: dict[str, str] = {}
    assignments: dict[str, dict[str, Any]] = {}
    for row in threads:
        root = find_project_root(row["cwd"], roots)
        if not root:
            continue
        hints[row["id"]] = root
        assignments[row["id"]] = {
            "projectKind": "local",
            "projectId": root,
            "path": root,
            "pendingCoreUpdate": False,
        }

    repaired = json.loads(json.dumps(state, ensure_ascii=False))
    repaired["electron-saved-workspace-roots"] = roots
    repaired["project-order"] = roots
    repaired["active-workspace-roots"] = []
    repaired["projectless-thread-ids"] = []
    repaired["thread-workspace-root-hints"] = hints
    repaired["thread-project-assignments"] = assignments

    return {
        "state": repaired,
        "roots": len(roots),
        "assignments": len(assignments),
        "prunedRoots": pruned_roots,
    }


def repair_global_state(
    home: Path,
    threads: list[sqlite3.Row],
    scan_parents: list[Path],
    keep_existing_roots: bool,
    dry_run: bool,
) -> dict[str, Any]:
    state_path = home / ".codex-global-state.json"
    if not state_path.exists():
        return {"state": {}, "roots": 0, "assignments": 0, "prunedRoots": []}
    plan = build_repaired_global_state(read_json(state_path), threads, scan_parents, keep_existing_roots)

    if not dry_run:
        ensure_writable(state_path)
        ensure_writable(home / ".codex-global-state.json.bak")
        write_json(state_path, plan["state"])
        write_json(home / ".codex-global-state.json.bak", plan["state"])
    return plan


def codex_processes_running() -> bool:
    if os.name != "nt":
        return False
    try:
        proc = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "@(Get-Process -Name Codex,codex -ErrorAction SilentlyContinue).Count",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError):
        return False
    try:
        return int(proc.stdout.strip() or "0") > 0
    except ValueError:
        return False


def ps_quote(value: Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def schedule_global_state_reapply_after_exit(
    home: Path,
    state: dict[str, Any],
    backup_dir: Path,
    timeout_minutes: int,
    dry_run: bool,
    launch: bool = False,
) -> Path | None:
    if dry_run or timeout_minutes <= 0:
        return None

    backup_dir.mkdir(parents=True, exist_ok=True)
    payload_path = backup_dir / "pending-global-state.json"
    script_path = backup_dir / "reapply-global-state-after-codex-exit.ps1"
    write_json(payload_path, state)

    state_path = home / ".codex-global-state.json"
    bak_path = home / ".codex-global-state.json.bak"
    script_path.write_text(
        "\n".join(
            [
                "$ErrorActionPreference = 'Stop'",
                f"$state = {ps_quote(state_path)}",
                f"$bak = {ps_quote(bak_path)}",
                f"$payload = {ps_quote(payload_path)}",
                f"$deadline = (Get-Date).AddMinutes({timeout_minutes})",
                "while ((Get-Date) -lt $deadline) {",
                "  $running = @(Get-Process -Name Codex,codex -ErrorAction SilentlyContinue)",
                "  if ($running.Count -eq 0) {",
                "    Start-Sleep -Seconds 5",
                "    $running = @(Get-Process -Name Codex,codex -ErrorAction SilentlyContinue)",
                "    if ($running.Count -eq 0) {",
                "      if (Test-Path -LiteralPath $state) { (Get-Item -LiteralPath $state).IsReadOnly = $false }",
                "      Copy-Item -LiteralPath $payload -Destination $state -Force",
                "      Copy-Item -LiteralPath $payload -Destination $bak -Force",
                "      Remove-Item -LiteralPath $MyInvocation.MyCommand.Path -Force -ErrorAction SilentlyContinue",
                "      exit 0",
                "    }",
                "  }",
                "  Start-Sleep -Seconds 5",
                "}",
                "exit 2",
                "",
            ]
        ),
        encoding="utf-8",
    )

    if launch:
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-WindowStyle",
                "Hidden",
                "-File",
                str(script_path),
            ],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    return script_path


def protect_global_state(home: Path, minutes: int, backup_dir: Path, dry_run: bool) -> bool:
    state_path = home / ".codex-global-state.json"
    if dry_run or minutes <= 0 or not state_path.exists():
        return False
    state_path.chmod(state_path.stat().st_mode & ~stat.S_IWRITE)

    unlock = backup_dir / "unlock-codex-global-state.ps1"
    unlock.write_text(
        "$state = '" + str(state_path).replace("'", "''") + "'\n"
        f"Start-Sleep -Seconds {minutes * 60}\n"
        "if (Test-Path -LiteralPath $state) { (Get-Item -LiteralPath $state).IsReadOnly = $false }\n",
        encoding="utf-8",
    )
    subprocess.Popen(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(unlock),
        ],
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return True


def distribution(con: sqlite3.Connection, field: str) -> dict[str, int]:
    rows = con.execute(f"SELECT {field}, count(*) FROM threads WHERE archived = 0 GROUP BY {field}").fetchall()
    return {str(row[0]): int(row[1]) for row in rows}


def find_codex_exe() -> str | None:
    candidates = []
    local_app = Path.home() / "AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/OpenAI/Codex/bin/codex.exe"
    candidates.append(local_app)
    found = shutil.which("codex")
    if found:
        candidates.append(Path(found))
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def verify_app_server(workdir: Path, use_state_db_only: bool, timeout_seconds: int) -> dict[str, Any]:
    codex = find_codex_exe()
    if not codex:
        return {"ok": False, "error": "codex executable not found"}

    proc = subprocess.Popen(
        [codex, "app-server", "--analytics-default-enabled"],
        cwd=str(workdir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    out_queue: queue.Queue[str] = queue.Queue()

    def reader() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            out_queue.put(line.rstrip("\n"))

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()

    try:
        assert proc.stdin is not None
        init = {
            "id": "init",
            "method": "initialize",
            "params": {
                "clientInfo": {"name": "probe", "title": "Probe", "version": "0.0.0"},
                "capabilities": {"experimentalApi": True, "optOutNotificationMethods": []},
            },
        }
        req = {
            "id": "verify-thread-list",
            "method": "thread/list",
            "params": {
                "limit": 100,
                "cursor": None,
                "sortKey": "updated_at",
                "modelProviders": None,
                "sourceKinds": [],
                "archived": False,
                "useStateDbOnly": use_state_db_only,
            },
        }
        proc.stdin.write(json.dumps(init, separators=(",", ":")) + "\n")
        proc.stdin.write(json.dumps(req, separators=(",", ":")) + "\n")
        proc.stdin.flush()

        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            try:
                line = out_queue.get(timeout=1)
            except queue.Empty:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("id") == "verify-thread-list":
                if obj.get("error"):
                    return {"ok": False, "error": obj["error"]}
                data = obj.get("result", {}).get("data", [])
                providers: dict[str, int] = {}
                sources: dict[str, int] = {}
                for item in data:
                    providers[item.get("modelProvider", "")] = providers.get(item.get("modelProvider", ""), 0) + 1
                    sources[item.get("source", "")] = sources.get(item.get("source", ""), 0) + 1
                return {
                    "ok": True,
                    "returned": len(data),
                    "providers": providers,
                    "sources": sources,
                    "nextCursor": obj.get("result", {}).get("nextCursor"),
                }
        return {"ok": False, "error": "thread/list timed out"}
    finally:
        if proc.poll() is None:
            proc.kill()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair local Codex Desktop history visibility.")
    parser.add_argument("--codex-home", type=Path, default=default_codex_home())
    parser.add_argument("--target", choices=["visible", "all"], default="visible")
    parser.add_argument("--unarchive", action="store_true", help="Set selected threads archived=0.")
    parser.add_argument("--provider", default="auto", help="Exact model_provider value accepted by current desktop app, or auto.")
    parser.add_argument("--source", default="auto", help="Exact source value accepted by current desktop app, or auto.")
    parser.add_argument("--thread-source", default="user")
    parser.add_argument("--scan-project-parent", type=Path, action="append", default=[])
    parser.add_argument(
        "--keep-existing-project-roots",
        action="store_true",
        help="Keep saved project roots that are not referenced by visible threads.",
    )
    parser.add_argument("--protect-state-minutes", type=int, default=0)
    parser.add_argument(
        "--after-exit-global-state",
        choices=["auto", "always", "never"],
        default="auto",
        help="Reapply pruned global state after Codex exits so running Desktop cannot overwrite it.",
    )
    parser.add_argument("--after-exit-timeout-minutes", type=int, default=720)
    parser.add_argument("--verify-app-server", action="store_true")
    parser.add_argument("--verify-timeout-seconds", type=int, default=90)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    home = args.codex_home
    db_path = home / "state_5.sqlite"
    if not db_path.exists():
        print(json.dumps({"ok": False, "error": f"missing {db_path}"}, ensure_ascii=False))
        return 2

    backup_dir = home / "history_sync_backups" / f"visibility-repair.{now_stamp()}"
    backup_state(home, backup_dir, args.dry_run)

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    try:
        provider, source = resolve_provider_and_source(con, args.provider, args.source)
        selected = fetch_threads(con, args.target)
        repair_database(
            con,
            selected,
            provider=provider,
            source=source,
            thread_source=args.thread_source,
            unarchive=args.unarchive,
            dry_run=args.dry_run,
        )
        visible = fetch_threads(con, "visible")
        changed, skipped_locked, missing = patch_rollout_files(
            visible,
            provider=provider,
            source=source,
            thread_source=args.thread_source,
            backup_dir=backup_dir,
            dry_run=args.dry_run,
        )
        rows = rebuild_history_files(home, visible, args.dry_run)
        codex_running = codex_processes_running()
        should_schedule_global_state = args.after_exit_global_state == "always" or (
            args.after_exit_global_state == "auto" and codex_running
        )
        write_global_state_now = not should_schedule_global_state
        global_state_repair = repair_global_state(
            home,
            visible,
            args.scan_project_parent,
            args.keep_existing_project_roots,
            args.dry_run or not write_global_state_now,
        )
        desired_global_state = global_state_repair["state"]
        after_exit_script = None
        if should_schedule_global_state:
            after_exit_script = schedule_global_state_reapply_after_exit(
                home,
                desired_global_state,
                backup_dir,
                args.after_exit_timeout_minutes,
                args.dry_run,
                launch=not args.dry_run,
            )
        protected = protect_global_state(home, args.protect_state_minutes, backup_dir, args.dry_run)

        result: dict[str, Any] = {
            "ok": True,
            "dryRun": bool(args.dry_run),
            "backupDir": None if args.dry_run else str(backup_dir),
            "resolvedProvider": provider,
            "resolvedSource": source,
            "selectedThreads": len(selected),
            "visibleThreads": len(visible),
            "sessionIndexRows": rows,
            "historyRows": rows,
            "rolloutMetaChanged": changed,
            "rolloutMetaSkippedLocked": skipped_locked,
            "rolloutMissing": missing,
            "projectRoots": global_state_repair["roots"],
            "projectMappings": global_state_repair["assignments"],
            "projectRootsPruned": len(global_state_repair["prunedRoots"]),
            "projectRootsPrunedValues": global_state_repair["prunedRoots"],
            "codexProcessesRunning": codex_running,
            "globalStateWrittenNow": (not args.dry_run) and write_global_state_now,
            "afterExitGlobalStateRequested": should_schedule_global_state,
            "afterExitGlobalStateScheduled": after_exit_script is not None,
            "afterExitGlobalStateScript": None if after_exit_script is None else str(after_exit_script),
            "providerDistribution": distribution(con, "model_provider"),
            "sourceDistribution": distribution(con, "source"),
            "stateProtected": protected,
        }
    finally:
        con.close()

    if args.verify_app_server:
        workdir = Path.cwd()
        result["threadListStateDbOnly"] = verify_app_server(workdir, True, args.verify_timeout_seconds)
        result["threadListScanMode"] = verify_app_server(workdir, False, args.verify_timeout_seconds)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
