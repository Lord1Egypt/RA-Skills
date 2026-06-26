#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import getpass
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

SEVERITY_ORDER = ["Critical", "High", "Medium", "Low", "Info"]
SEVERITY_RANK = {name: idx for idx, name in enumerate(SEVERITY_ORDER)}
NO_ISSUES_PHRASES = (
    "no findings",
    "no issues",
    "all clear",
    "passed",
    "clean",
    "nothing found",
    "0 findings",
)

ACTIVE_SKILLS_ROOT = Path(
    os.environ.get("OPENCLAW_SKILLS_DIR", "~/.openclaw/skills")
).expanduser()
QUARANTINE_ROOT = Path(
    os.environ.get("OPENCLAW_QUARANTINE_DIR", "~/.openclaw/skills-quarantine")
).expanduser()
WORKSPACE_ROOT = Path(
    os.environ.get("OPENCLAW_WORKSPACE_DIR", "~/.openclaw")
).expanduser()
STAGE_ROOT = Path(
    os.environ.get("OPENCLAW_STAGE_DIR", str(WORKSPACE_ROOT / ".skill_stage"))
).expanduser()


def stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def sanitize(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    cleaned = re.sub(r"-+", "-", cleaned).strip(".-_")
    return cleaned or "skill"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def extract_skill_name(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        try:
            for line in skill_md.read_text(encoding="utf-8", errors="ignore").splitlines()[:120]:
                match = re.match(r"^name:\s*(.+?)\s*$", line)
                if match:
                    return sanitize(match.group(1))
        except OSError:
            pass
    return sanitize(skill_dir.name)


def scanner_base() -> list[str]:
    custom = os.environ.get("SENTINAL_SCANNER_CMD")
    if custom:
        return shlex.split(custom)
    if shutil.which("uv"):
        return ["uv", "run", "skill-scanner"]
    if shutil.which("skill-scanner"):
        return ["skill-scanner"]
    raise SystemExit(
        "skill-scanner not found. Install it or set SENTINAL_SCANNER_CMD."
    )


def clawhub_base() -> list[str]:
    custom = os.environ.get("SENTINAL_CLAWHUB_CMD")
    if custom:
        return shlex.split(custom)
    if shutil.which("npx"):
        return ["npx", "-y", "clawhub"]
    raise SystemExit("clawhub not found. Install node+npx or set SENTINAL_CLAWHUB_CMD.")


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    print("+", shlex.join(cmd))
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None)


def default_report_path(label: str, kind: str) -> Path:
    label = sanitize(label)
    return Path(tempfile.gettempdir()) / f"sentinal-{kind}-{label}-{stamp()}.md"


def parse_report(text: str) -> tuple[dict[str, int], str]:
    counts = {name: 0 for name in SEVERITY_ORDER}
    severity_seen = False

    heading_re = re.compile(r"^\s*#{1,6}\s*(Critical|High|Medium|Low|Info)\b", re.I)
    bullet_re = re.compile(r"^\s*(?:[-*]|\d+\.)\s*(Critical|High|Medium|Low|Info)\b", re.I)
    summary_re = re.compile(r"^\s*(Critical|High|Medium|Low|Info)\s*[:\-]\s*(\d+)\b", re.I)

    for line in text.splitlines():
        matched = False
        for rx in (summary_re, heading_re, bullet_re):
            match = rx.match(line)
            if not match:
                continue
            severity = match.group(1).title()
            if rx is summary_re:
                counts[severity] += int(match.group(2))
            else:
                counts[severity] += 1
            severity_seen = True
            matched = True
            break
        if matched:
            continue

    lowered = text.lower()
    if counts["Critical"] or counts["High"]:
        return counts, "blocked"
    if counts["Medium"] or counts["Low"] or counts["Info"]:
        return counts, "warning"
    if any(phrase in lowered for phrase in NO_ISSUES_PHRASES):
        return counts, "clean"
    if severity_seen:
        return counts, "clean"
    return counts, "unknown"


def summarize(counts: dict[str, int]) -> str:
    parts = [f"{name}={counts[name]}" for name in SEVERITY_ORDER if counts[name]]
    return ", ".join(parts) if parts else "no severity markers"


def read_report(report_path: Path | None) -> tuple[dict[str, int], str, str | None]:
    if report_path is None:
        return {name: 0 for name in SEVERITY_ORDER}, "unknown", None
    if not report_path.exists():
        return {name: 0 for name in SEVERITY_ORDER}, "unknown", None
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    counts, verdict = parse_report(text)
    return counts, verdict, text


def scan_with_scanner(target: Path, *, bulk: bool = False, report_path: Path | None = None) -> tuple[int, Path, dict[str, int], str]:
    ensure_dir(report_path.parent if report_path else Path(tempfile.gettempdir()))
    report_path = report_path or default_report_path(target.name, "bulk" if bulk else "single")
    cmd = scanner_base() + [
        "scan-all" if bulk else "scan",
        str(target),
        "--format",
        "markdown",
        "--detailed",
        "--output",
        str(report_path),
    ]
    result = run(cmd)
    if result.returncode != 0:
        return result.returncode, report_path, {name: 0 for name in SEVERITY_ORDER}, "scanner-error"
    counts, verdict, _ = read_report(report_path)
    return 0, report_path, counts, verdict


def find_installed_skill_dir(stage_skills_dir: Path, expected_slug: str | None = None) -> Path:
    if not stage_skills_dir.exists():
        raise SystemExit(f"Expected staged skill directory not found: {stage_skills_dir}")

    dirs = [p for p in stage_skills_dir.iterdir() if p.is_dir()]
    if not dirs:
        raise SystemExit(f"No staged skill directory found under {stage_skills_dir}")

    if expected_slug:
        normalized = sanitize(expected_slug)
        for candidate in dirs:
            if sanitize(candidate.name) == normalized:
                return candidate

    skill_md_dirs = [p for p in dirs if (p / "SKILL.md").exists()]
    if len(skill_md_dirs) == 1:
        return skill_md_dirs[0]
    if len(dirs) == 1:
        return dirs[0]

    names = ", ".join(sorted(p.name for p in dirs))
    raise SystemExit(f"Could not determine staged skill directory inside {stage_skills_dir}: {names}")


def copy_skill_tree(source: Path, destination_root: Path, *, force: bool = False) -> Path:
    skill_name = extract_skill_name(source)
    destination = destination_root / skill_name
    if destination.exists():
        if not force:
            raise SystemExit(f"Destination already exists: {destination}. Use --force to replace it.")
        shutil.rmtree(destination)
    ensure_dir(destination_root)
    shutil.copytree(source, destination)
    return destination


def quarantine_skill(source: Path, *, force: bool = False) -> Path:
    resolved_source = source.resolve()
    active_root = ACTIVE_SKILLS_ROOT.resolve()
    try:
        resolved_source.relative_to(active_root)
    except ValueError as exc:
        raise SystemExit(f"Refusing to quarantine a path outside the active skill tree: {source}") from exc

    quarantine_root = ensure_dir(QUARANTINE_ROOT)
    destination = quarantine_root / f"{extract_skill_name(source)}-{stamp()}"
    if destination.exists():
        if not force:
            raise SystemExit(f"Quarantine destination already exists: {destination}")
        shutil.rmtree(destination)
    shutil.move(str(source), str(destination))
    return destination


def print_result(target: Path, report_path: Path, counts: dict[str, int], verdict: str) -> None:
    print(f"Report: {report_path}")
    print(f"Target: {target}")
    print(f"Severity: {summarize(counts)}")
    print(f"Verdict: {verdict}")


def emit_bullets(title: str, items: list[str]) -> None:
    print(f"{title}:")
    if not items:
        print("- none")
        return
    for item in items:
        print(f"- {item}")


def emit_report(verified: list[str], suspected: list[str], unknown: list[str], next_step: str) -> None:
    emit_bullets("What is verified", verified)
    emit_bullets("What is suspected", suspected)
    emit_bullets("What is unknown", unknown)
    print("Recommended next step:")
    print(f"- {next_step}")


def fetch_json(url: str, timeout: float = 2.0) -> dict | None:
    request = urllib.request.Request(url, headers={"User-Agent": "sentinal/0.4.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
        return json.loads(payload)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError, json.JSONDecodeError):
        return None


def run_capture(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    print("+", shlex.join(cmd))
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)


def cmd_scan(args: argparse.Namespace) -> int:
    source = Path(args.path).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Path does not exist: {source}")
    report_path = Path(args.report).expanduser() if args.report else None
    rc, report_path, counts, verdict = scan_with_scanner(source, bulk=False, report_path=report_path)
    print_result(source, report_path, counts, verdict)
    if rc != 0:
        return rc
    return 2 if verdict == "blocked" else 0


def cmd_scan_all(args: argparse.Namespace) -> int:
    source = Path(args.path).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Path does not exist: {source}")
    report_path = Path(args.report).expanduser() if args.report else None
    rc, report_path, counts, verdict = scan_with_scanner(source, bulk=True, report_path=report_path)
    print_result(source, report_path, counts, verdict)
    if rc != 0:
        return rc
    return 2 if verdict == "blocked" else 0


def cmd_scan_install_local(args: argparse.Namespace) -> int:
    source = Path(args.path).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Path does not exist: {source}")
    rc, report_path, counts, verdict = scan_with_scanner(source, bulk=False, report_path=None)
    print_result(source, report_path, counts, verdict)
    if rc != 0:
        return rc
    if verdict == "blocked":
        return 2
    destination = copy_skill_tree(source, Path(args.dest_root).expanduser(), force=args.force)
    print(f"Installed: {destination}")
    return 0


def cmd_scan_install_clawhub(args: argparse.Namespace) -> int:
    stage_root = ensure_dir(Path(args.stage_root).expanduser())
    stage_dir = Path(tempfile.mkdtemp(prefix=f"{sanitize(args.slug)}-", dir=str(stage_root)))
    clawhub = clawhub_base() + ["--workdir", str(stage_dir), "--dir", "skills", "install", args.slug]
    if args.version:
        clawhub.extend(["--version", args.version])
    result = run(clawhub)
    if result.returncode != 0:
        return result.returncode

    staged_skills_dir = stage_dir / "skills"
    candidate = find_installed_skill_dir(staged_skills_dir, args.slug)
    rc, report_path, counts, verdict = scan_with_scanner(candidate, bulk=False, report_path=None)
    print_result(candidate, report_path, counts, verdict)
    if rc != 0:
        return rc
    if verdict == "blocked":
        print(f"Blocked staged ClawHub install: {candidate}")
        return 2

    if args.apply:
        destination = copy_skill_tree(candidate, Path(args.dest_root).expanduser(), force=args.force)
        print(f"Installed: {destination}")
    else:
        print(f"Staged install retained at: {candidate}")
    return 0


def cmd_auto_scan(args: argparse.Namespace) -> int:
    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Path does not exist: {root}")
    rc, report_path, counts, verdict = scan_with_scanner(root, bulk=True, report_path=None)
    print_result(root, report_path, counts, verdict)
    if rc != 0:
        return rc
    return 2 if verdict == "blocked" else 0


def cmd_quarantine(args: argparse.Namespace) -> int:
    source = Path(args.path).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Path does not exist: {source}")
    destination = quarantine_skill(source, force=args.force)
    print(f"Quarantined: {destination}")
    return 0


def cmd_openclaw_health(args: argparse.Namespace) -> int:
    endpoint = args.endpoint or os.environ.get("OPENCLAW_CDP_URL", "http://127.0.0.1:9223")
    endpoint = endpoint.rstrip("/")
    version_url = endpoint if endpoint.endswith("/json/version") else f"{endpoint}/json/version"
    targets_url = endpoint if endpoint.endswith("/json/list") else f"{endpoint}/json/list"

    version = fetch_json(version_url)
    targets = fetch_json(targets_url) or []

    if version is None:
        emit_report(
            verified=[],
            suspected=[f"OpenClaw browser bridge is not reachable at {version_url}"],
            unknown=["Whether the browser session is available or healthy"],
            next_step="Start or reconnect the Chrome/Bridge session, then re-run the check.",
        )
        return 2

    browser_label = version.get("Browser") or version.get("Protocol-Version") or "unknown browser"
    websocket = version.get("webSocketDebuggerUrl") or "not exposed"
    verified = [
        f"OpenClaw browser bridge is reachable at {version_url}",
        f"Browser: {browser_label}",
        f"Targets reported: {len(targets)}",
        f"WebSocket debugger URL: {websocket}",
    ]
    suspected = []
    if len(targets) == 0:
        suspected.append("No active tabs were reported by the browser bridge")
    unknown = ["Session poisoning and task-specific context health cannot be proven from the bridge alone"]
    emit_report(
        verified=verified,
        suspected=suspected,
        unknown=unknown,
        next_step="If the bridge looks healthy but a task is misbehaving, start a fresh browser session and abandon the poisoned thread.",
    )
    return 1 if suspected else 0


def cmd_hermes_health(args: argparse.Namespace) -> int:
    hermes_home = Path(args.hermes_home).expanduser()
    critical: list[str] = []
    suspected: list[str] = []
    verified: list[str] = []
    unknown: list[str] = []

    if hermes_home.exists():
        verified.append(f"Hermes home exists: {hermes_home}")
    else:
        critical.append(f"Hermes home is missing: {hermes_home}")

    for rel in ["skills", "memory"]:
        path = hermes_home / rel
        if path.exists():
            verified.append(f"Present: {path}")
        else:
            suspected.append(f"Missing expected Hermes directory: {path}")

    for rel in ["config.yaml", "google_token.json"]:
        path = hermes_home / rel
        if path.exists():
            verified.append(f"Present: {path}")
        else:
            suspected.append(f"Missing optional Hermes file: {path}")

    tools = ["git", "gh", "python3"]
    for tool in tools:
        found = shutil.which(tool)
        if found:
            verified.append(f"Tool available: {tool} -> {found}")
        else:
            critical.append(f"Tool not found on PATH: {tool}")

    unknown.append("Cron/background job state is not inspected here; use a dedicated scheduler check if needed")
    unknown.append("MCP gateway health is not directly verified by this local file check")

    emit_report(
        verified=verified,
        suspected=suspected + critical,
        unknown=unknown,
        next_step="If critical Hermes files or tools are missing, restore them before trusting the session; otherwise continue in a clean session.",
    )
    return 2 if critical else (1 if suspected else 0)


def cmd_host_guard(args: argparse.Namespace) -> int:
    verified: list[str] = []
    suspected: list[str] = []
    unknown: list[str] = []

    verified.extend([
        f"Host: {platform.system()} {platform.release()} ({platform.machine()})",
        f"User: {getpass.getuser()}",
        f"Python: {sys.version.split()[0]}",
    ])

    ps_cmd = ["ps", "-eo", "pid,ppid,user,comm,args", "--sort=-%cpu"]
    ps_result = run_capture(ps_cmd)
    if ps_result.returncode == 0 and ps_result.stdout:
        lines = ps_result.stdout.splitlines()
        verified.append(f"Process snapshot captured ({max(len(lines) - 1, 0)} rows)")
        for line in lines[1:6]:
            verified.append(f"ps: {line.strip()}")
    else:
        suspected.append("Could not capture process snapshot with ps")

    listener_cmd: list[str] | None = None
    if shutil.which("ss"):
        listener_cmd = ["ss", "-ltnp"]
    elif shutil.which("netstat"):
        listener_cmd = ["netstat", "-ltnp"]

    if listener_cmd:
        listener_result = run_capture(listener_cmd)
        if listener_result.returncode == 0 and listener_result.stdout:
            lines = [line for line in listener_result.stdout.splitlines() if line.strip()]
            verified.append(f"Listener snapshot captured ({len(lines)} lines)")
            for line in lines[1:6]:
                verified.append(f"listener: {line.strip()}")
        else:
            suspected.append("Could not capture listening sockets")
    else:
        unknown.append("No ss/netstat binary available to inspect listening sockets")

    disk_cmd = ["df", "-h", "/"]
    disk_result = run_capture(disk_cmd)
    if disk_result.returncode == 0 and disk_result.stdout:
        for line in disk_result.stdout.splitlines()[1:2]:
            verified.append(f"root disk: {line.strip()}")
    else:
        unknown.append("Could not read root filesystem usage")

    emit_report(
        verified=verified,
        suspected=suspected,
        unknown=unknown,
        next_step="Review any unexpected listeners or privileged processes before changing the host.",
    )
    return 1 if suspected else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Active Defense Sentinal helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="Scan a single skill path")
    p_scan.add_argument("path", help="Skill directory to scan")
    p_scan.add_argument("--report", help="Optional report file path")
    p_scan.set_defaults(func=cmd_scan)

    p_scan_all = sub.add_parser("scan-all", help="Scan a directory of skills")
    p_scan_all.add_argument("path", help="Directory containing skills to scan")
    p_scan_all.add_argument("--report", help="Optional report file path")
    p_scan_all.set_defaults(func=cmd_scan_all)

    p_install_local = sub.add_parser(
        "scan-install-local",
        help="Scan a local skill folder and install it into the active skill tree when safe",
    )
    p_install_local.add_argument("path", help="Local skill directory")
    p_install_local.add_argument(
        "--dest-root",
        default=str(ACTIVE_SKILLS_ROOT),
        help="Active skills root (default: ~/.openclaw/skills)",
    )
    p_install_local.add_argument("--force", action="store_true", help="Replace an existing destination")
    p_install_local.set_defaults(func=cmd_scan_install_local)

    p_install_clawhub = sub.add_parser(
        "scan-install-clawhub",
        help="Stage-install a ClawHub skill, scan it, then optionally copy it into the active tree",
    )
    p_install_clawhub.add_argument("slug", help="ClawHub skill slug")
    p_install_clawhub.add_argument("--version", help="Optional version override")
    p_install_clawhub.add_argument(
        "--stage-root",
        default=str(STAGE_ROOT),
        help="Stage root (default: ~/.openclaw/.skill_stage)",
    )
    p_install_clawhub.add_argument(
        "--dest-root",
        default=str(ACTIVE_SKILLS_ROOT),
        help="Active skills root (default: ~/.openclaw/skills)",
    )
    p_install_clawhub.add_argument("--apply", action="store_true", help="Copy the safe staged skill into the active tree")
    p_install_clawhub.add_argument("--force", action="store_true", help="Replace an existing destination")
    p_install_clawhub.set_defaults(func=cmd_scan_install_clawhub)

    p_auto = sub.add_parser("auto-scan", help="Scan the active user skills tree")
    p_auto.add_argument(
        "path",
        nargs="?",
        default=str(ACTIVE_SKILLS_ROOT),
        help="Skill tree to scan (default: ~/.openclaw/skills)",
    )
    p_auto.set_defaults(func=cmd_auto_scan)

    p_quarantine = sub.add_parser("quarantine", help="Move an installed skill into quarantine")
    p_quarantine.add_argument("path", help="Installed skill directory to quarantine")
    p_quarantine.add_argument("--force", action="store_true", help="Replace an existing quarantine destination")
    p_quarantine.set_defaults(func=cmd_quarantine)

    p_openclaw = sub.add_parser("openclaw-health", help="Check the OpenClaw browser bridge and active tab surface")
    p_openclaw.add_argument(
        "--endpoint",
        help="Browser bridge base URL (default: OPENCLAW_CDP_URL or http://127.0.0.1:9223)",
    )
    p_openclaw.set_defaults(func=cmd_openclaw_health)

    p_hermes = sub.add_parser("hermes-health", help="Check Hermes runtime directories and core tools")
    p_hermes.add_argument(
        "--hermes-home",
        default=str(Path.home() / ".hermes"),
        help="Hermes home directory (default: ~/.hermes)",
    )
    p_hermes.set_defaults(func=cmd_hermes_health)

    p_host = sub.add_parser("host-guard", help="Capture local host telemetry for triage")
    p_host.set_defaults(func=cmd_host_guard)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
