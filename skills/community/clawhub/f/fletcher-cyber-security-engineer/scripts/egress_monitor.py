#!/usr/bin/env python3
"""Outbound (egress) TCP connection monitor for OpenClaw.

Lists established TCP connections, keeps the ones that are genuinely outbound
traffic from OpenClaw's own processes, and checks each destination against the
egress allowlist (~/.openclaw/security/egress_allowlist.json).

What is evaluated
- Scope: by default only OpenClaw processes (the gateway, anything named
  ``openclaw``/``openclaw-*``, and their child processes). Use ``--scope all``
  to evaluate every process on the host.
- Direction: connections accepted on a port the process is listening on are
  inbound and are not egress.
- Destination: loopback, link-local, multicast and unspecified addresses never
  leave the host/segment and are ignored (``--include-local`` to keep them).

Allowlist rules (JSON array of objects; every given field must match)
- ``protocol``   "tcp" (default)
- ``port``       single port, or ``ports`` for a list
- ``command``    process name, case-insensitive (optional)
- ``host``       hostname or IP address, or ``hosts`` for a list
- ``cidr``       network in CIDR notation, or a list of them
- ``host_regex`` regular expression tested against the remote IP and against
                 the allowlisted hostnames that resolve to it
- ``comment``    free text, shown as the matched rule in reports

Network use: allowlisted hostnames are resolved through the system DNS
resolver so they can be compared with the IP addresses the OS reports
(disable with ``--no-resolve``). Resolved addresses are remembered for seven
days in ~/.openclaw/security/egress-dns-cache.json so rotating CDN addresses
do not cause false findings. No other network calls are made.
"""
import argparse
import ipaddress
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple

SECURITY_DIR = Path.home() / ".openclaw" / "security"
DEFAULT_ALLOWLIST = SECURITY_DIR / "egress_allowlist.json"
DEFAULT_DNS_CACHE = SECURITY_DIR / "egress-dns-cache.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

DEFAULT_GATEWAY_PORT = 18789
DNS_CACHE_MAX_AGE_DAYS = 7
DNS_TIMEOUT_SECONDS = 3.0
MAX_REGEX_LENGTH = 200
EXIT_FINDINGS = 3

Connection = Dict[str, object]
Listener = Tuple[int, int]  # (pid, local port)
ProcessTable = Dict[int, Tuple[int, str]]  # pid -> (parent pid, command line)
IPAddress = "ipaddress._BaseAddress"
Resolver = Callable[[str], Set[str]]


# --------------------------------------------------------------------------
# Command-line interface
# --------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Check OpenClaw's outbound TCP connections against the egress allowlist."
    )
    p.add_argument("--allowlist", default=str(DEFAULT_ALLOWLIST), help="Allowlist JSON file")
    p.add_argument(
        "--scope",
        choices=("openclaw", "all"),
        default="openclaw",
        help="Which processes to evaluate: OpenClaw's own (default) or every process on the host",
    )
    p.add_argument(
        "--include-process",
        action="append",
        default=[],
        metavar="REGEX",
        help="Also treat processes whose command line matches REGEX as OpenClaw (repeatable)",
    )
    p.add_argument(
        "--include-local",
        action="store_true",
        help="Also evaluate loopback, link-local and multicast destinations",
    )
    p.add_argument(
        "--no-resolve",
        action="store_true",
        help="Do not query DNS for allowlisted hostnames (previously cached answers are still used)",
    )
    p.add_argument("--dns-cache", default=str(DEFAULT_DNS_CACHE), help="DNS answer cache file")
    p.add_argument(
        "--fail-on-findings",
        action="store_true",
        help=f"Exit with status {EXIT_FINDINGS} when unapproved connections are found",
    )
    p.add_argument("--json", action="store_true", help="JSON output")
    return p.parse_args(argv)


# --------------------------------------------------------------------------
# Collecting connections, listeners and processes
# --------------------------------------------------------------------------

def _run(cmd: List[str], empty_ok: bool = False) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        # lsof exits 1 when nothing matches the filter; that is an empty result, not a failure.
        if empty_ok and not proc.stdout.strip() and not proc.stderr.strip():
            return ""
        if not proc.stdout.strip():
            raise RuntimeError(proc.stderr.strip() or f"Failed to run {cmd[0]}")
    return proc.stdout


def split_host_port(token: str) -> Tuple[Optional[str], Optional[int]]:
    """Split "1.2.3.4:443", "[::1]:443" or "fe80::1%en0:443" into (host, port)."""
    token = token.strip()
    if not token:
        return None, None
    if token.startswith("["):
        m = re.match(r"^\[(.*)\]:(\d+)$", token)
        if not m:
            return None, None
        return m.group(1), int(m.group(2))
    host, sep, port = token.rpartition(":")
    if not sep or not host or not port.isdigit():
        return None, None
    return host, int(port)


def _connection(
    command: str,
    pid: object,
    user: Optional[str],
    local: Tuple[Optional[str], Optional[int]],
    remote: Tuple[Optional[str], Optional[int]],
) -> Connection:
    pid_text = str(pid)
    return {
        "command": command,
        "pid": int(pid_text) if pid_text.isdigit() else pid_text,
        "user": user,
        "local_host": local[0],
        "local_port": local[1],
        "remote_host": remote[0],
        "remote_port": remote[1],
        "protocol": "tcp",
    }


def _dedupe(conns: Iterable[Connection]) -> List[Connection]:
    out: List[Connection] = []
    seen = set()
    for c in conns:
        key = (c["command"], c["pid"], c["local_port"], c["remote_host"], c["remote_port"])
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def _lsof_name(parts: List[str]) -> str:
    # lsof appends the TCP state as its own token: "... a:1->b:443 (ESTABLISHED)".
    return parts[-2] if parts[-1].startswith("(") else parts[-1]


def parse_lsof(text: str) -> List[Connection]:
    conns: List[Connection] = []
    for ln in text.splitlines():
        parts = ln.split()
        if len(parts) < 9 or parts[0] == "COMMAND":
            continue
        name = _lsof_name(parts)
        if "->" not in name:
            continue
        local_text, remote_text = name.split("->", 1)
        remote = split_host_port(remote_text)
        if remote[1] is None:
            continue
        conns.append(_connection(parts[0], parts[1], parts[2], split_host_port(local_text), remote))
    return _dedupe(conns)


def parse_lsof_listeners(text: str) -> Set[Listener]:
    listeners: Set[Listener] = set()
    for ln in text.splitlines():
        parts = ln.split()
        if len(parts) < 9 or parts[0] == "COMMAND" or not parts[1].isdigit():
            continue
        _, port = split_host_port(_lsof_name(parts))
        if port is not None:
            listeners.add((int(parts[1]), port))
    return listeners


_SS_USERS_RE = re.compile(r'users:\(\("([^"]+)",pid=(\d+)')
_SS_HEADER_PREFIXES = ("State", "Recv-Q", "Netid")


def _ss_endpoints(ln: str) -> List[Tuple[str, int]]:
    """Address:port tokens of an ss line, in order (local first, then peer)."""
    endpoints: List[Tuple[str, int]] = []
    for token in ln.split():
        if token.startswith("users:"):
            break
        host, port = split_host_port(token)
        if host is not None and port is not None:
            endpoints.append((host, port))
    return endpoints


def parse_ss(text: str) -> List[Connection]:
    conns: List[Connection] = []
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith(_SS_HEADER_PREFIXES):
            continue
        endpoints = _ss_endpoints(ln)
        if len(endpoints) < 2:
            continue
        m = _SS_USERS_RE.search(ln)
        command = m.group(1) if m else "unknown"
        pid: object = m.group(2) if m else "unknown"
        conns.append(_connection(command, pid, None, endpoints[0], endpoints[1]))
    return _dedupe(conns)


def parse_ss_listeners(text: str) -> Set[Listener]:
    listeners: Set[Listener] = set()
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith(_SS_HEADER_PREFIXES):
            continue
        endpoints = _ss_endpoints(ln)
        m = _SS_USERS_RE.search(ln)
        if endpoints and m:
            listeners.add((int(m.group(2)), endpoints[0][1]))
    return listeners


def parse_netstat_windows(text: str) -> List[Connection]:
    conns: List[Connection] = []
    for ln in text.splitlines():
        parts = ln.split()
        if len(parts) < 5 or parts[0].upper() != "TCP" or parts[3].upper() != "ESTABLISHED":
            continue
        remote = split_host_port(parts[2])
        if remote[1] is None:
            continue
        conns.append(_connection("unknown", parts[4], None, split_host_port(parts[1]), remote))
    return _dedupe(conns)


def parse_netstat_windows_listeners(text: str) -> Set[Listener]:
    listeners: Set[Listener] = set()
    for ln in text.splitlines():
        parts = ln.split()
        if len(parts) < 5 or parts[0].upper() != "TCP" or parts[3].upper() != "LISTENING":
            continue
        _, port = split_host_port(parts[1])
        if port is not None and parts[4].isdigit():
            listeners.add((int(parts[4]), port))
    return listeners


def collect_connections() -> Tuple[List[Connection], Set[Listener], str]:
    """Return (established connections, listening sockets, tool used)."""
    if shutil.which("lsof"):
        established = _run(["lsof", "-nP", "-iTCP", "-sTCP:ESTABLISHED"], empty_ok=True)
        listening = _run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"], empty_ok=True)
        return parse_lsof(established), parse_lsof_listeners(listening), "lsof"
    if sys.platform.startswith("linux") and shutil.which("ss"):
        established = _run(["ss", "-tnp", "state", "established"])
        listening = _run(["ss", "-tlnp"])
        return parse_ss(established), parse_ss_listeners(listening), "ss"
    if sys.platform.startswith("win") and shutil.which("netstat"):
        text = _run(["netstat", "-ano", "-p", "tcp"])
        return parse_netstat_windows(text), parse_netstat_windows_listeners(text), "netstat"
    raise RuntimeError("No supported connection tool found (lsof/ss/netstat)")


def parse_ps(text: str) -> ProcessTable:
    table: ProcessTable = {}
    for ln in text.splitlines():
        m = re.match(r"\s*(\d+)\s+(\d+)\s+(.*)$", ln)
        if m:
            table[int(m.group(1))] = (int(m.group(2)), m.group(3).strip())
    return table


def read_process_table() -> ProcessTable:
    """pid -> (parent pid, command line) for every process on the host."""
    if sys.platform.startswith("win"):
        script = (
            "Get-CimInstance Win32_Process | "
            "Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
        )
        rows = json.loads(_run(["powershell", "-NoProfile", "-Command", script]) or "[]")
        if isinstance(rows, dict):
            rows = [rows]
        table: ProcessTable = {}
        for row in rows:
            command = str(row.get("CommandLine") or row.get("Name") or "")
            table[int(row["ProcessId"])] = (int(row.get("ParentProcessId") or 0), command)
        return table
    return parse_ps(_run(["ps", "-axo", "pid=,ppid=,command="]))


# --------------------------------------------------------------------------
# Scoping to OpenClaw's own processes
# --------------------------------------------------------------------------

# Deliberately case-sensitive: the executable is always lower-case, while folders named
# "OpenClaw ..." show up as stray tokens when a path containing spaces is split.
_OPENCLAW_EXECUTABLE_RE = re.compile(r"^openclaw(\.(mjs|cjs|js))?$|^openclaw\.(cmd|exe)$")
_OPENCLAW_TITLE_RE = re.compile(r"^openclaw(-[a-z0-9_-]+)?$")


def is_openclaw_command(command: str) -> bool:
    """True for the OpenClaw CLI/gateway, however it was launched.

    Matches the process titles OpenClaw sets ("openclaw", "openclaw-gateway"),
    the ``openclaw`` executable or entry script among the leading arguments
    ("node /path/openclaw.mjs gateway"), and anything run from the installed
    package. A path that merely contains "openclaw" (a project folder, this
    skill's own scripts under ~/.openclaw) does not match.
    """
    tokens = command.split()
    for index, token in enumerate(tokens[:3]):
        normalized = token.replace("\\", "/")
        if "/node_modules/openclaw/" in normalized.lower():
            return True
        base = normalized.rstrip("/").rsplit("/", 1)[-1]
        if base.lower().endswith((".cmd", ".exe")):
            base = base.lower()  # Windows file names are case-insensitive
        if _OPENCLAW_EXECUTABLE_RE.match(base):
            return True
        if index == 0 and _OPENCLAW_TITLE_RE.match(base):
            return True
    return False


def gateway_port(config_path: Path = OPENCLAW_CONFIG) -> int:
    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        port = cfg.get("gateway", {}).get("port")
        if isinstance(port, int) and 0 < port < 65536:
            return port
    except Exception:
        pass
    return DEFAULT_GATEWAY_PORT


def openclaw_pids(
    table: ProcessTable,
    listeners: Set[Listener],
    gateway_listen_port: int,
    extra_patterns: Iterable["re.Pattern[str]"] = (),
    exclude_roots: Iterable[int] = (),
) -> Set[int]:
    """OpenClaw's processes: the gateway, named OpenClaw processes, and all their descendants.

    ``exclude_roots`` are pids that must never be taken for OpenClaw by name (the
    monitor itself). They are still in scope when OpenClaw started them.
    """
    extra = list(extra_patterns)
    excluded = set(exclude_roots)
    roots = {pid for pid, port in listeners if port == gateway_listen_port}
    for pid, (_, command) in table.items():
        if pid in excluded:
            continue
        if is_openclaw_command(command) or any(p.search(command) for p in extra):
            roots.add(pid)

    children: Dict[int, List[int]] = {}
    for pid, (ppid, _) in table.items():
        children.setdefault(ppid, []).append(pid)

    scoped: Set[int] = set()
    stack = list(roots)
    while stack:
        pid = stack.pop()
        if pid in scoped:
            continue
        scoped.add(pid)
        stack.extend(children.get(pid, []))
    return scoped


# --------------------------------------------------------------------------
# Destination classification
# --------------------------------------------------------------------------

def parse_ip(host: object) -> Optional["ipaddress._BaseAddress"]:
    text = str(host or "").strip().strip("[]")
    text = text.split("%", 1)[0]  # drop an IPv6 zone id such as "%en0"
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return None
    mapped = getattr(ip, "ipv4_mapped", None)
    return mapped if mapped is not None else ip


def is_local_destination(host: object) -> bool:
    """Destinations that never leave this host or network segment."""
    ip = parse_ip(host)
    if ip is None:
        return str(host or "").strip().lower() == "localhost"
    return bool(ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_unspecified)


# --------------------------------------------------------------------------
# Allowlist rules
# --------------------------------------------------------------------------

class Rule:
    """One compiled allowlist entry."""

    def __init__(self, index: int, raw: Dict[str, object]) -> None:
        self.index = index
        self.raw = raw
        self.protocol = str(raw.get("protocol") or "tcp").lower()
        self.ports = self._ports(raw)
        self.command = str(raw.get("command")).lower() if raw.get("command") else None
        self.networks: List["ipaddress._BaseNetwork"] = []
        self.hostnames: List[str] = []
        self.regex: Optional["re.Pattern[str]"] = None
        self.errors: List[str] = []
        self.constrains_host = False

        for cidr in _as_list(raw.get("cidr")):
            self.constrains_host = True
            try:
                self.networks.append(ipaddress.ip_network(str(cidr), strict=False))
            except ValueError:
                self.errors.append(f"invalid cidr {cidr!r}")

        for host in _as_list(raw.get("host")) + _as_list(raw.get("hosts")):
            self.constrains_host = True
            ip = parse_ip(host)
            if ip is not None:
                self.networks.append(ipaddress.ip_network(f"{ip}/{ip.max_prefixlen}"))
            else:
                self.hostnames.append(_normalize_hostname(str(host)))

        pattern = raw.get("host_regex")
        if pattern:
            self.constrains_host = True
            pattern = str(pattern)
            if len(pattern) > MAX_REGEX_LENGTH:
                self.errors.append(f"host_regex longer than {MAX_REGEX_LENGTH} characters")
            else:
                try:
                    self.regex = re.compile(pattern)
                except re.error as exc:
                    self.errors.append(f"invalid host_regex: {exc}")
                else:
                    # Hostnames spelled out in the pattern are resolved like "host" entries.
                    for name in hostnames_in_regex(pattern, self.regex):
                        if name not in self.hostnames:
                            self.hostnames.append(name)

    @staticmethod
    def _ports(raw: Dict[str, object]) -> Optional[Set[int]]:
        values = _as_list(raw.get("port")) + _as_list(raw.get("ports"))
        ports: Set[int] = set()
        for value in values:
            try:
                ports.add(int(value))  # type: ignore[arg-type]
            except (TypeError, ValueError):
                continue
        if "port" in raw or "ports" in raw:
            return ports
        return None

    @property
    def label(self) -> str:
        comment = self.raw.get("comment")
        return str(comment) if comment else f"rule {self.index + 1}"

    def matches(self, conn: Connection, resolved: Dict[str, Set[str]]) -> bool:
        if self.errors:
            return False  # a rule that could not be compiled never allows anything
        if self.protocol != str(conn.get("protocol") or "tcp").lower():
            return False
        if self.ports is not None and conn.get("remote_port") not in self.ports:
            return False
        if self.command and self.command != str(conn.get("command") or "").lower():
            return False
        if not self.constrains_host:
            return True

        host = str(conn.get("remote_host") or "")
        ip = parse_ip(host)
        if ip is not None:
            if any(ip.version == net.version and ip in net for net in self.networks):
                return True
            if any(str(ip) in resolved.get(name, ()) for name in self.hostnames):
                return True
        elif _normalize_hostname(host) in self.hostnames:
            return True
        if self.regex is not None:
            candidates = [host] + names_for_ip(ip, resolved)
            if any(self.regex.search(c) for c in candidates):
                return True
        return False


def _as_list(value: object) -> List[object]:
    if value is None or value == "":
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def _normalize_hostname(name: str) -> str:
    return name.strip().rstrip(".").lower()


_HOSTNAME_IN_REGEX_RE = re.compile(
    r"(?<![A-Za-z0-9.-])(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,}(?![A-Za-z0-9-])"
)


def hostnames_in_regex(pattern: str, compiled: "re.Pattern[str]") -> List[str]:
    """Literal hostnames written inside a host_regex, e.g. ``^api\\.openai\\.com$``.

    Only names the pattern itself accepts are returned, so this can never
    widen what the rule's author allowed.
    """
    candidates = _HOSTNAME_IN_REGEX_RE.findall(pattern.replace("\\.", "."))
    names = {_normalize_hostname(c) for c in candidates}
    return sorted(n for n in names if compiled.search(n))


def names_for_ip(ip: Optional["ipaddress._BaseAddress"], resolved: Dict[str, Set[str]]) -> List[str]:
    if ip is None:
        return []
    return sorted(name for name, addresses in resolved.items() if str(ip) in addresses)


def load_allowlist(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [r for r in raw if isinstance(r, dict)] if isinstance(raw, list) else []


def compile_rules(raw_rules: List[Dict[str, object]]) -> List[Rule]:
    return [Rule(i, raw) for i, raw in enumerate(raw_rules)]


# --------------------------------------------------------------------------
# Hostname resolution (with a small on-disk memory of past answers)
# --------------------------------------------------------------------------

def system_resolver(hostname: str) -> Set[str]:
    addresses: Set[str] = set()
    for info in socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM):
        ip = parse_ip(info[4][0])
        if ip is not None:
            addresses.add(str(ip))
    return addresses


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(ts: datetime) -> str:
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def load_dns_cache(path: Path, now: datetime) -> Dict[str, Dict[str, str]]:
    """hostname -> {ip: last seen}, without entries older than the retention window."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        hosts = raw.get("hosts", {}) if isinstance(raw, dict) else {}
    except Exception:
        return {}
    cutoff = now - timedelta(days=DNS_CACHE_MAX_AGE_DAYS)
    cache: Dict[str, Dict[str, str]] = {}
    for name, addresses in hosts.items() if isinstance(hosts, dict) else []:
        if not isinstance(addresses, dict):
            continue
        fresh: Dict[str, str] = {}
        for address, seen in addresses.items():
            try:
                seen_at = datetime.strptime(str(seen), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if seen_at >= cutoff and parse_ip(address) is not None:
                fresh[str(address)] = str(seen)
        if fresh:
            cache[str(name)] = fresh
    return cache


def save_dns_cache(path: Path, cache: Dict[str, Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"version": 1, "hosts": cache}, f, indent=2, sort_keys=True)
            f.write("\n")
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, str(path))
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def resolve_hostnames(
    hostnames: Iterable[str],
    cache: Dict[str, Dict[str, str]],
    now: datetime,
    resolver: Optional[Resolver] = system_resolver,
    timeout: float = DNS_TIMEOUT_SECONDS,
) -> Tuple[Dict[str, Set[str]], List[str]]:
    """Resolve hostnames, merging fresh answers into ``cache``.

    Returns (hostname -> addresses, hostnames that could not be resolved now).
    Pass ``resolver=None`` to rely on cached answers only.
    """
    names = sorted(set(hostnames))
    failed: List[str] = []
    if resolver is not None and names:
        pool = ThreadPoolExecutor(max_workers=min(8, len(names)))
        try:
            futures = {name: pool.submit(resolver, name) for name in names}
            for name, future in futures.items():
                try:
                    addresses = future.result(timeout=timeout)
                except (FutureTimeoutError, OSError, UnicodeError):
                    failed.append(name)
                    continue
                stamp = _iso(now)
                entry = cache.setdefault(name, {})
                for address in addresses:
                    entry[address] = stamp
        finally:
            pool.shutdown(wait=False)
    resolved = {name: set(cache.get(name, {})) for name in names}
    return resolved, failed


# --------------------------------------------------------------------------
# Evaluation
# --------------------------------------------------------------------------

def evaluate(
    conns: List[Connection],
    listeners: Set[Listener],
    scoped_pids: Optional[Set[int]],
    rules: List[Rule],
    resolved: Dict[str, Set[str]],
    include_local: bool = False,
) -> Tuple[List[Connection], List[Dict[str, object]], Dict[str, int]]:
    """Filter to real egress and check it. ``scoped_pids=None`` means every process."""
    summary = {
        "connections_seen": len(conns),
        "out_of_scope": 0,
        "ignored_inbound": 0,
        "ignored_local": 0,
        "evaluated": 0,
        "allowed": 0,
        "unapproved": 0,
    }
    evaluated: List[Connection] = []
    findings: List[Dict[str, object]] = []

    for conn in conns:
        pid = conn.get("pid")
        if scoped_pids is not None and pid not in scoped_pids:
            summary["out_of_scope"] += 1
            continue
        if (pid, conn.get("local_port")) in listeners:
            summary["ignored_inbound"] += 1
            continue
        if not include_local and is_local_destination(conn.get("remote_host")):
            summary["ignored_local"] += 1
            continue

        names = names_for_ip(parse_ip(conn.get("remote_host")), resolved)
        matched = next((r for r in rules if r.matches(conn, resolved)), None)
        record = dict(conn)
        record["remote_names"] = names
        record["allowed"] = matched is not None
        record["matched_rule"] = matched.label if matched else None
        evaluated.append(record)

        summary["evaluated"] += 1
        if matched is not None:
            summary["allowed"] += 1
            continue
        summary["unapproved"] += 1
        findings.append(
            {
                "type": "unapproved-egress",
                "severity": "medium",
                "command": conn.get("command"),
                "pid": pid,
                "remote_host": conn.get("remote_host"),
                "remote_port": conn.get("remote_port"),
                "remote_names": names,
                "recommendation": "Add to egress allowlist with justification or terminate the connection.",
            }
        )
    return evaluated, findings, summary


def build_report(args: argparse.Namespace) -> Dict[str, object]:
    warnings: List[str] = []
    now = _utc_now()
    allow_path = Path(args.allowlist).expanduser()
    cache_path = Path(args.dns_cache).expanduser()

    conns, listeners, tool = collect_connections()

    try:
        table = read_process_table()
    except Exception as exc:
        table = {}
        warnings.append(f"Process list unavailable ({exc}); child processes of OpenClaw may be missed.")

    # Windows netstat reports only pids; fill in process names from the process table.
    for conn in conns:
        if conn["command"] == "unknown" and conn["pid"] in table:
            command = table[conn["pid"]][1]  # type: ignore[index]
            conn["command"] = (command.split() or ["unknown"])[0].replace("\\", "/").rsplit("/", 1)[-1]

    scoped: Optional[Set[int]] = None
    processes: List[Dict[str, object]] = []
    if args.scope == "openclaw":
        extra = [re.compile(p) for p in args.include_process]
        scoped = openclaw_pids(table, listeners, gateway_port(), extra, exclude_roots={os.getpid()})
        processes = [
            {"pid": pid, "command": table.get(pid, (0, "unknown"))[1][:160]} for pid in sorted(scoped)
        ]
        if not scoped:
            warnings.append("No OpenClaw processes are running; there was nothing to evaluate.")

    rules = compile_rules(load_allowlist(allow_path))
    for rule in rules:
        for error in rule.errors:
            warnings.append(f"Allowlist {rule.label} is ignored: {error}.")

    cache = load_dns_cache(cache_path, now)
    hostnames = [name for rule in rules for name in rule.hostnames]
    resolved, failed = resolve_hostnames(
        hostnames, cache, now, resolver=None if args.no_resolve else system_resolver
    )
    for name in failed:
        warnings.append(f"Could not resolve {name}; relying on previously seen addresses.")
    if hostnames and not args.no_resolve:
        try:
            save_dns_cache(cache_path, cache)
        except Exception as exc:
            warnings.append(f"Could not update DNS cache {cache_path}: {exc}")

    evaluated, findings, summary = evaluate(
        conns, listeners, scoped, rules, resolved, include_local=args.include_local
    )
    return {
        "status": "ok",
        "generated_at_utc": _iso(now),
        "tool": tool,
        "scope": args.scope,
        "allowlist_file": str(allow_path),
        "allowlist_rules_count": len(rules),
        "processes": processes,
        "resolved_hosts": {name: sorted(addresses) for name, addresses in sorted(resolved.items())},
        "summary": summary,
        "connections": evaluated,
        "findings": findings,
        "warnings": warnings,
    }


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def _destination(row: Dict[str, object]) -> str:
    host = str(row.get("remote_host"))
    if ":" in host:
        host = f"[{host}]"
    names = row.get("remote_names") or []
    suffix = f" ({', '.join(names)})" if names else ""  # type: ignore[arg-type]
    return f"{host}:{row.get('remote_port')}{suffix}"


def render_text(report: Dict[str, object]) -> str:
    if report.get("status") != "ok":
        return f"Egress monitor failed: {report.get('error')}"
    s: Dict[str, int] = report["summary"]  # type: ignore[assignment]
    scope = "OpenClaw processes" if report["scope"] == "openclaw" else "all processes"
    lines = [
        f"Egress monitor: {scope}, via {report['tool']}",
        f"Allowlist: {report['allowlist_file']} ({report['allowlist_rules_count']} rule(s))",
        "",
        f"Connections seen on host : {s['connections_seen']}",
        f"  outside scope          : {s['out_of_scope']}",
        f"  inbound (ignored)      : {s['ignored_inbound']}",
        f"  local-only (ignored)   : {s['ignored_local']}",
        f"Evaluated                : {s['evaluated']}",
        f"  allowed                : {s['allowed']}",
        f"  unapproved             : {s['unapproved']}",
    ]
    connections: List[Dict[str, object]] = report["connections"]  # type: ignore[assignment]
    if connections:
        lines += ["", "Evaluated connections:"]
        for c in connections:
            verdict = f"allowed by {c['matched_rule']}" if c["allowed"] else "UNAPPROVED"
            lines.append(f"  {c['command']} (pid {c['pid']}) -> {_destination(c)}: {verdict}")
    for warning in report.get("warnings") or []:  # type: ignore[union-attr]
        lines.append(f"Warning: {warning}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        report = build_report(args)
    except Exception as exc:
        report = {"status": "error", "error": str(exc), "connections": [], "findings": []}

    print(json.dumps(report, indent=2) if args.json else render_text(report))
    if report.get("status") != "ok":
        return 1
    if args.fail_on_findings and report.get("findings"):
        return EXIT_FINDINGS
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
