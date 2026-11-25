#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


INSECURE_PORT_RECOMMENDATIONS = {
    20: "Use SFTP (22) or FTPS (990) instead of FTP data.",
    21: "Use SFTP (22) or FTPS (990) instead of FTP control.",
    23: "Use SSH (22) instead of Telnet.",
    69: "Use HTTPS-based transfer APIs instead of TFTP.",
    80: "Use HTTPS (443) instead of HTTP.",
    110: "Use POP3S (995) instead of POP3.",
    143: "Use IMAPS (993) instead of IMAP.",
    389: "Use LDAPS (636) instead of LDAP.",
    512: "Disable r-commands and use SSH (22).",
    513: "Disable r-commands and use SSH (22).",
    514: "Use TLS-secured syslog transport.",
}

DEFAULT_APPROVED_PATH = Path.home() / ".openclaw" / "security" / "approved_ports.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenClaw port monitor and risk recommender")
    parser.add_argument(
        "--approved-file",
        default=str(DEFAULT_APPROVED_PATH),
        help="JSON file of approved listening ports/services",
    )
    parser.add_argument(
        "--include-udp",
        action="store_true",
        help="Also list UDP sockets (off by default: desktop systems keep many open for discovery services)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output only",
    )
    return parser.parse_args()


def _run_lsof(selector: List[str]) -> str:
    # "+c 0" prints full process names; lsof otherwise cuts them to 9 characters.
    proc = subprocess.run(["lsof", "+c", "0", "-nP"] + selector, capture_output=True, text=True)
    if proc.returncode != 0:
        # lsof exits 1 when nothing matches; that is an empty result, not a failure.
        if not proc.stdout.strip() and not proc.stderr.strip():
            return ""
        if not proc.stdout.strip():
            raise RuntimeError(proc.stderr.strip() or "Failed to run lsof")
    return proc.stdout


def run_lsof() -> str:
    return _run_lsof(["-iTCP", "-sTCP:LISTEN"])


def run_lsof_udp() -> str:
    return _run_lsof(["-iUDP"])


def run_ss(udp: bool = False) -> str:
    cmd = ["ss", "-lunp" if udp else "-ltnp"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "Failed to run ss")
    return proc.stdout


def run_netstat_windows() -> str:
    cmd = ["netstat", "-ano", "-p", "tcp"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "Failed to run netstat")
    return proc.stdout


def parse_name(name: str) -> Tuple[Optional[str], Optional[int]]:
    name = name.replace("(LISTEN)", "").strip()
    # *:22, 127.0.0.1:631, [::1]:8080
    if name.startswith("["):
        match = re.search(r"\[(.*?)\]:(\d+)$", name)
    else:
        match = re.search(r"(.+):(\d+)$", name)
    if not match:
        return None, None
    host = match.group(1)
    port = int(match.group(2))
    return host, port


def parse_lsof_output(text: str, protocol: str = "tcp") -> List[Dict[str, object]]:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) <= 1:
        return []
    entries: List[Dict[str, object]] = []
    seen = set()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 9:
            continue
        command = parts[0]
        pid = parts[1]
        user = parts[2]
        name = parts[-2] if parts[-1] == "(LISTEN)" else parts[-1]
        if "->" in name:
            continue  # a connected socket, not a listener
        host, port = parse_name(name)
        if port is None:
            continue
        entry = {
            "command": command,
            "pid": int(pid) if pid.isdigit() else pid,
            "user": user,
            "host": host,
            "port": port,
            "protocol": protocol,
        }
        dedupe_key = (entry["command"], entry["pid"], entry["host"], entry["port"], entry["protocol"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        entries.append(entry)
    return entries


def parse_ss_output(text: str, protocol: str = "tcp") -> List[Dict[str, object]]:
    lines = [line for line in text.splitlines() if line.strip()]
    entries: List[Dict[str, object]] = []
    seen = set()
    state = "LISTEN" if protocol == "tcp" else "UNCONN"
    for line in lines[1:]:
        if state not in line:
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        local = parts[3]
        host, port = parse_name(local)
        if port is None:
            continue
        cmd_match = re.search(r'users:\(\("([^"]+)",pid=(\d+)', line)
        command = cmd_match.group(1) if cmd_match else "unknown"
        pid = int(cmd_match.group(2)) if cmd_match else "unknown"
        entry = {
            "command": command,
            "pid": pid,
            "user": None,
            "host": host,
            "port": port,
            "protocol": protocol,
        }
        dedupe_key = (entry["command"], entry["pid"], entry["host"], entry["port"], entry["protocol"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        entries.append(entry)
    return entries


def parse_netstat_windows_output(text: str) -> List[Dict[str, object]]:
    entries: List[Dict[str, object]] = []
    seen = set()
    for line in text.splitlines():
        if not line.strip().startswith("TCP"):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        local = parts[1]
        state = parts[3]
        pid = parts[4]
        if state.upper() != "LISTENING":
            continue
        host, port = parse_name(local)
        if port is None:
            continue
        entry = {
            "command": "unknown",
            "pid": int(pid) if pid.isdigit() else pid,
            "user": None,
            "host": host,
            "port": port,
            "protocol": "tcp",
        }
        dedupe_key = (entry["command"], entry["pid"], entry["host"], entry["port"], entry["protocol"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        entries.append(entry)
    return entries


def collect_entries(include_udp: bool = False) -> Tuple[List[Dict[str, object]], str]:
    if shutil.which("lsof"):
        entries = parse_lsof_output(run_lsof())
        if include_udp:
            entries += parse_lsof_output(run_lsof_udp(), protocol="udp")
        return entries, "lsof"
    if sys.platform.startswith("linux") and shutil.which("ss"):
        entries = parse_ss_output(run_ss())
        if include_udp:
            entries += parse_ss_output(run_ss(udp=True), protocol="udp")
        return entries, "ss"
    if sys.platform.startswith("win") and shutil.which("netstat"):
        return parse_netstat_windows_output(run_netstat_windows()), "netstat"
    raise RuntimeError("No supported port listing tool found (lsof/ss/netstat)")


def load_approved_ports(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Approved ports file must be a JSON array.")
    normalized: List[Dict[str, object]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if "port" not in item:
            continue
        normalized.append(item)
    return normalized


PUBLIC_HOSTS = ("*", "0.0.0.0", "::")
ANY_PORT = "*"
_LSOF_NAME_WIDTH = 9  # lsof's default process-name width, used by older baselines


def commands_match(rule_command: object, entry_command: object) -> bool:
    """Process names match exactly, or one is the 9-character form lsof used to print."""
    rule, entry = str(rule_command).lower(), str(entry_command).lower()
    if rule == entry:
        return True
    shorter, longer = sorted((rule, entry), key=len)
    return len(shorter) == _LSOF_NAME_WIDTH and longer.startswith(shorter)


def matching_rule(entry: Dict[str, object], approved: List[Dict[str, object]]) -> Optional[Dict[str, object]]:
    for rule in approved:
        if rule.get("port") == ANY_PORT:
            # For services that pick a new port each time they start. The process name is
            # then the only thing identifying the service, so it is required.
            if not rule.get("command"):
                continue
        else:
            try:
                if int(rule.get("port")) != int(entry["port"]):
                    continue
            except (TypeError, ValueError):
                continue
        rule_proto = str(rule.get("protocol", "tcp")).lower()
        if rule_proto != str(entry["protocol"]).lower():
            continue
        rule_cmd = rule.get("command")
        if rule_cmd and not commands_match(rule_cmd, entry["command"]):
            continue
        return rule
    return None


def is_approved(entry: Dict[str, object], approved: List[Dict[str, object]]) -> bool:
    return matching_rule(entry, approved) is not None


def build_findings(entries: List[Dict[str, object]], approved: List[Dict[str, object]]) -> List[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    seen = set()

    def add(finding: Dict[str, object]) -> None:
        # One finding per service: the same port is often listed once for IPv4 and once for IPv6.
        key = (finding["type"], finding["port"], finding["protocol"], finding["command"])
        if key not in seen:
            seen.add(key)
            findings.append(finding)

    for entry in entries:
        port = int(entry["port"])
        host = str(entry.get("host") or "")
        base = {"port": port, "protocol": entry.get("protocol", "tcp"), "command": entry["command"]}
        rule = matching_rule(entry, approved)

        if rule is None:
            add(
                dict(
                    base,
                    severity="medium",
                    type="unapproved-port",
                    message="Listening port is not in approved baseline.",
                    recommendation="Approve it with business justification or close the service.",
                )
            )

        if port in INSECURE_PORT_RECOMMENDATIONS and base["protocol"] == "tcp":
            add(
                dict(
                    base,
                    severity="high",
                    type="insecure-port",
                    message="Insecure protocol/port detected.",
                    recommendation=INSECURE_PORT_RECOMMENDATIONS[port],
                )
            )

        # Listening on every interface is accepted only when the baseline rule says so.
        if host in PUBLIC_HOSTS and not (rule is not None and rule.get("allow_public") is True):
            add(
                dict(
                    base,
                    severity="medium",
                    type="public-bind",
                    message="Service listens on all interfaces.",
                    recommendation=(
                        "Bind to localhost or a restricted interface, or set \"allow_public\": true on its "
                        "approved-ports rule if the exposure is required."
                    ),
                )
            )
    return findings


def output_text(report: Dict[str, object]) -> None:
    print("Port Monitoring Report")
    print(f"Listening services: {len(report['listening_services'])}")
    print(f"Findings: {len(report['findings'])}")
    if report["findings"]:
        print("")
        for finding in report["findings"]:
            print(
                f"- [{finding['severity'].upper()}] {finding['type']} "
                f"port {finding['port']} ({finding['command']}): {finding['recommendation']}"
            )


def main() -> int:
    args = parse_args()
    approved_path = Path(args.approved_file).expanduser()
    try:
        entries, tool_used = collect_entries(include_udp=args.include_udp)
        approved = load_approved_ports(approved_path)
        findings = build_findings(entries, approved)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 1

    report = {
        "status": "ok",
        "approved_file": str(approved_path),
        "approved_rules_count": len(approved),
        "tool": tool_used,
        "protocols": ["tcp", "udp"] if args.include_udp else ["tcp"],
        "summary": {
            "listening_services": len(entries),
            "unapproved": sum(1 for f in findings if f["type"] == "unapproved-port"),
            "insecure": sum(1 for f in findings if f["type"] == "insecure-port"),
            "public": sum(1 for f in findings if f["type"] == "public-bind"),
        },
        "listening_services": entries,
        "findings": findings,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        output_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
