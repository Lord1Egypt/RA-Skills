#!/usr/bin/env python3
"""
docker-compose-linter — Lint docker-compose.yml files for security, best practices, and port conflicts.
Pure stdlib, no external dependencies.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Lightweight YAML-like parser
# ---------------------------------------------------------------------------

def _strip_comment(line: str) -> str:
    """Remove inline comment from a line (naive: not inside quotes)."""
    in_single = False
    in_double = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == '#' and not in_single and not in_double:
            return line[:i].rstrip()
    return line.rstrip()


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _unquote(s: str) -> str:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


class ParseNode:
    """Tree node for parsed YAML-like structure."""
    __slots__ = ("key", "value", "children", "line_no")

    def __init__(self, key: str, value: Optional[str], line_no: int):
        self.key = key
        self.value = value
        self.children: List["ParseNode"] = []
        self.line_no = line_no

    def __repr__(self):
        return f"ParseNode({self.key!r}, {self.value!r}, children={len(self.children)})"


def _parse_lines(lines: List[Tuple[int, int, str]]) -> List[ParseNode]:
    """
    Recursive descent: lines is list of (line_no, indent, content).
    Returns list of top-level ParseNodes.
    """
    nodes: List[ParseNode] = []
    i = 0
    while i < len(lines):
        line_no, indent, content = lines[i]

        # List item
        if content.startswith("- "):
            val = content[2:].strip()
            node = ParseNode("__list_item__", _unquote(val) if val else None, line_no)
            i += 1
            # Collect child lines at deeper indent
            child_lines = []
            while i < len(lines) and lines[i][1] > indent:
                child_lines.append(lines[i])
                i += 1
            if child_lines:
                node.children = _parse_lines(child_lines)
            nodes.append(node)
            continue

        # Bare list item with no value (just "- ")
        if content == "-":
            node = ParseNode("__list_item__", None, line_no)
            i += 1
            nodes.append(node)
            continue

        # Key: value  or  Key:
        if ":" in content:
            colon = content.index(":")
            key = content[:colon].strip()
            rest = content[colon + 1:].strip()
            value = _unquote(rest) if rest else None
            node = ParseNode(key, value, line_no)
            i += 1
            # Collect child lines at deeper indent
            child_lines = []
            while i < len(lines) and lines[i][1] > indent:
                child_lines.append(lines[i])
                i += 1
            if child_lines:
                node.children = _parse_lines(child_lines)
            nodes.append(node)
            continue

        # Bare value (shouldn't appear much but handle gracefully)
        node = ParseNode("__value__", content, line_no)
        nodes.append(node)
        i += 1

    return nodes


def parse_compose(text: str) -> List[ParseNode]:
    """Parse a docker-compose file text into a tree of ParseNodes."""
    raw_lines = text.splitlines()
    processed: List[Tuple[int, int, str]] = []

    for lineno, raw in enumerate(raw_lines, start=1):
        # Skip empty lines and pure comment lines
        stripped = _strip_comment(raw)
        if not stripped.strip():
            continue
        content = stripped.lstrip()
        if not content:
            continue
        ind = _indent(stripped)
        processed.append((lineno, ind, content))

    return _parse_lines(processed)


def find_node(nodes: List[ParseNode], key: str) -> Optional[ParseNode]:
    for n in nodes:
        if n.key == key:
            return n
    return None


def node_value(nodes: List[ParseNode], key: str) -> Optional[str]:
    n = find_node(nodes, key)
    return n.value if n else None


def list_items(node: ParseNode) -> List[str]:
    """Return all __list_item__ values under this node."""
    return [c.value for c in node.children if c.key == "__list_item__" and c.value is not None]


def child_keys(node: ParseNode) -> List[str]:
    return [c.key for c in node.children if c.key != "__list_item__"]


# ---------------------------------------------------------------------------
# Issue dataclass
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


@dataclass
class Issue:
    rule: str
    severity: str  # error | warning | info
    service: Optional[str]
    message: str
    line: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "service": self.service,
            "message": self.message,
            "line": self.line,
        }


# ---------------------------------------------------------------------------
# Lint rules
# ---------------------------------------------------------------------------

SECRET_PATTERN = re.compile(
    r'(?i)(password|passwd|secret|api[_-]?key|private[_-]?key|token|auth[_-]?key|access[_-]?key)\s*=\s*.+',
)

TAG_LATEST_PATTERN = re.compile(r'^[^:]+(:latest)?$')


def _image_has_latest_or_no_tag(image: str) -> bool:
    """Return True if image uses :latest or has no tag at all."""
    image = image.strip()
    # Remove registry prefix (host:port/...)
    # Remove digest
    if "@sha256:" in image:
        return False
    if ":" not in image.split("/")[-1]:
        return True  # no tag
    tag = image.rsplit(":", 1)[-1]
    return tag == "latest"


def lint_compose(
    nodes: List[ParseNode],
    ignore_rules: Optional[List[str]] = None,
    min_severity: str = "info",
) -> List[Issue]:
    issues: List[Issue] = []
    ignore_rules = ignore_rules or []
    min_sev_order = SEVERITY_ORDER.get(min_severity, 2)

    def add(rule, severity, service, message, line=None):
        if rule in ignore_rules:
            return
        if SEVERITY_ORDER.get(severity, 2) > min_sev_order:
            return
        issues.append(Issue(rule=rule, severity=severity, service=service, message=message, line=line))

    # ---- Rule: no-version ----
    version_node = find_node(nodes, "version")
    if not version_node:
        add("no-version", "info", None, "No 'version:' key found in compose file.")
    elif version_node.value and version_node.value.startswith("2"):
        add("no-version", "info", None, f"Version '{version_node.value}' is legacy (v2.x). Consider v3+.")

    # ---- Get services ----
    services_node = find_node(nodes, "services")
    if not services_node:
        return issues

    # ---- Rule: duplicate-service ----
    svc_names: List[str] = []
    seen: set = set()
    for svc_node in services_node.children:
        if svc_node.key == "__list_item__":
            continue
        name = svc_node.key
        if name in seen:
            add("duplicate-service", "error", name,
                f"Duplicate service name '{name}'.", svc_node.line_no)
        seen.add(name)
        svc_names.append(name)

    # ---- Port conflict detection ----
    host_ports: Dict[str, List[str]] = {}  # port -> [service]

    for svc_node in services_node.children:
        if svc_node.key == "__list_item__":
            continue
        svc_name = svc_node.key
        svc_children = svc_node.children

        # Collect image
        image_val = node_value(svc_children, "image")
        build_node = find_node(svc_children, "build")

        # ---- Rule: latest-tag ----
        if image_val and _image_has_latest_or_no_tag(image_val):
            add("latest-tag", "warning", svc_name,
                f"Image '{image_val}' uses ':latest' tag or has no tag. Pin to a specific version.",
                find_node(svc_children, "image").line_no if find_node(svc_children, "image") else None)
        elif not image_val and not build_node:
            add("latest-tag", "warning", svc_name,
                f"Service '{svc_name}' has no image or build directive.")

        # ---- Rule: no-healthcheck ----
        hc_node = find_node(svc_children, "healthcheck")
        if not hc_node:
            add("no-healthcheck", "warning", svc_name,
                f"Service '{svc_name}' has no healthcheck defined.")

        # ---- Rule: no-restart-policy ----
        restart_val = node_value(svc_children, "restart")
        if not restart_val:
            add("no-restart-policy", "warning", svc_name,
                f"Service '{svc_name}' has no restart policy.")

        # ---- Rule: privileged-mode ----
        priv_val = node_value(svc_children, "privileged")
        priv_node = find_node(svc_children, "privileged")
        if priv_val and priv_val.lower() == "true":
            add("privileged-mode", "error", svc_name,
                f"Service '{svc_name}' runs in privileged mode. This is a serious security risk.",
                priv_node.line_no if priv_node else None)

        # ---- Rule: host-network ----
        nm_val = node_value(svc_children, "network_mode")
        nm_node = find_node(svc_children, "network_mode")
        if nm_val and nm_val.lower() == "host":
            add("host-network", "warning", svc_name,
                f"Service '{svc_name}' uses network_mode: host (security risk).",
                nm_node.line_no if nm_node else None)

        # ---- Rule: hardcoded-env ----
        env_node = find_node(svc_children, "environment")
        if env_node:
            for item in list_items(env_node):
                if SECRET_PATTERN.search(item):
                    add("hardcoded-env", "warning", svc_name,
                        f"Service '{svc_name}' appears to have a hardcoded secret in environment: '{item[:60]}'.",
                        env_node.line_no)
                    break
            # Also check map-style env
            for env_child in env_node.children:
                if env_child.key != "__list_item__" and env_child.value:
                    combined = f"{env_child.key}={env_child.value}"
                    if SECRET_PATTERN.search(combined):
                        add("hardcoded-env", "warning", svc_name,
                            f"Service '{svc_name}' appears to have a hardcoded secret: '{combined[:60]}'.",
                            env_child.line_no)
                        break

        # ---- Rule: root-user ----
        user_val = node_value(svc_children, "user")
        if not user_val:
            add("root-user", "warning", svc_name,
                f"Service '{svc_name}' has no 'user:' defined (runs as root by default).")

        # ---- Rule: no-resource-limits ----
        deploy_node = find_node(svc_children, "deploy")
        has_limits = False
        if deploy_node:
            res_node = find_node(deploy_node.children, "resources")
            if res_node:
                lim_node = find_node(res_node.children, "limits")
                if lim_node:
                    has_limits = True
        if not has_limits:
            add("no-resource-limits", "info", svc_name,
                f"Service '{svc_name}' has no memory/CPU resource limits (deploy.resources.limits).")

        # ---- Rule: no-logging ----
        log_node = find_node(svc_children, "logging")
        if not log_node:
            add("no-logging", "info", svc_name,
                f"Service '{svc_name}' has no logging configuration.")

        # ---- Rule: bind-mount-relative ----
        vol_node = find_node(svc_children, "volumes")
        if vol_node:
            for item in list_items(vol_node):
                # Format: source:target or just target
                parts = item.split(":")
                if parts:
                    src = parts[0]
                    # Relative if doesn't start with / or ~ and contains a path separator or .
                    if src and not src.startswith("/") and not src.startswith("~") and ("/" in src or src.startswith(".")):
                        add("bind-mount-relative", "info", svc_name,
                            f"Service '{svc_name}' uses a relative bind mount path: '{src}'.",
                            vol_node.line_no)
                        break

        # ---- Collect ports for conflict detection ----
        ports_node = find_node(svc_children, "ports")
        if ports_node:
            for item in list_items(ports_node):
                # Format: "host:container" or "host:container/proto" or just "container"
                item_clean = item.strip().strip('"').strip("'")
                # Handle IP:host:container
                parts = item_clean.split(":")
                if len(parts) >= 2:
                    host_port = parts[-2].split("/")[0]  # strip protocol
                    # Skip if it's a range
                    if "-" not in host_port:
                        if host_port not in host_ports:
                            host_ports[host_port] = []
                        host_ports[host_port].append(svc_name)
                # Long-form port mapping (map style)
            for port_child in ports_node.children:
                if port_child.key == "published":
                    hp = port_child.value
                    if hp and "-" not in hp:
                        if hp not in host_ports:
                            host_ports[hp] = []
                        host_ports[hp].append(svc_name)

        # ---- Rule: missing-depends-on (basic heuristic) ----
        # If service references another service name in its volumes or environment
        # but has no depends_on — we skip this complex heuristic for now and just
        # check if network aliases or links exist without depends_on.
        links_node = find_node(svc_children, "links")
        depends_node = find_node(svc_children, "depends_on")
        if links_node and not depends_node:
            add("missing-depends-on", "info", svc_name,
                f"Service '{svc_name}' uses 'links' but has no 'depends_on'.",
                links_node.line_no)

    # ---- Rule: port-conflict ----
    for port, svcs in host_ports.items():
        if len(svcs) > 1:
            add("port-conflict", "error", None,
                f"Host port {port} is mapped by multiple services: {', '.join(svcs)}.")

    return issues


# ---------------------------------------------------------------------------
# Service/port extraction helpers
# ---------------------------------------------------------------------------

@dataclass
class ServiceInfo:
    name: str
    image: Optional[str]
    build: Optional[str]
    ports: List[str]
    restart: Optional[str]
    line: int


def extract_services(nodes: List[ParseNode]) -> List[ServiceInfo]:
    services_node = find_node(nodes, "services")
    if not services_node:
        return []
    result = []
    for svc_node in services_node.children:
        if svc_node.key == "__list_item__":
            continue
        svc_children = svc_node.children
        image = node_value(svc_children, "image")
        build_node = find_node(svc_children, "build")
        build_val = None
        if build_node:
            build_val = build_node.value or node_value(build_node.children, "context") or "(build)"
        ports_node = find_node(svc_children, "ports")
        ports = list_items(ports_node) if ports_node else []
        restart = node_value(svc_children, "restart")
        result.append(ServiceInfo(
            name=svc_node.key,
            image=image,
            build=build_val,
            ports=ports,
            restart=restart,
            line=svc_node.line_no,
        ))
    return result


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

SEVERITY_ICONS = {"error": "[ERROR]", "warning": "[WARN] ", "info": "[INFO] "}
SEVERITY_COLORS = {
    "error": "\033[91m",
    "warning": "\033[93m",
    "info": "\033[96m",
    "reset": "\033[0m",
}


def _use_color() -> bool:
    return sys.stdout.isatty()


def _color(text: str, severity: str) -> str:
    if not _use_color():
        return text
    c = SEVERITY_COLORS.get(severity, "")
    r = SEVERITY_COLORS["reset"]
    return f"{c}{text}{r}"


def format_issues_text(issues: List[Issue]) -> str:
    if not issues:
        return "No issues found."
    lines = []
    for iss in issues:
        icon = SEVERITY_ICONS.get(iss.severity, "[    ]")
        svc = f" [{iss.service}]" if iss.service else ""
        loc = f" (line {iss.line})" if iss.line else ""
        rule = f" <{iss.rule}>"
        line = f"{_color(icon, iss.severity)}{svc}{loc}{rule} {iss.message}"
        lines.append(line)
    return "\n".join(lines)


def format_issues_json(issues: List[Issue]) -> str:
    return json.dumps([i.to_dict() for i in issues], indent=2)


def format_issues_markdown(issues: List[Issue]) -> str:
    if not issues:
        return "_No issues found._"
    lines = ["| Severity | Rule | Service | Line | Message |",
             "|----------|------|---------|------|---------|"]
    for iss in issues:
        svc = iss.service or "-"
        loc = str(iss.line) if iss.line else "-"
        msg = iss.message.replace("|", "\\|")
        lines.append(f"| {iss.severity} | `{iss.rule}` | {svc} | {loc} | {msg} |")
    return "\n".join(lines)


def format_services_text(services: List[ServiceInfo]) -> str:
    if not services:
        return "No services found."
    lines = []
    for svc in services:
        src = svc.image or f"build:{svc.build}" or "?"
        restart = svc.restart or "none"
        ports_str = ", ".join(svc.ports) if svc.ports else "no ports"
        lines.append(f"  {svc.name:<20} image={src}  restart={restart}  ports=[{ports_str}]")
    return "\n".join(lines)


def format_services_json(services: List[ServiceInfo]) -> str:
    return json.dumps([
        {"name": s.name, "image": s.image, "build": s.build,
         "ports": s.ports, "restart": s.restart, "line": s.line}
        for s in services
    ], indent=2)


def format_services_markdown(services: List[ServiceInfo]) -> str:
    if not services:
        return "_No services found._"
    lines = ["| Service | Image/Build | Ports | Restart |",
             "|---------|-------------|-------|---------|"]
    for svc in services:
        src = svc.image or f"build:{svc.build}" or "?"
        restart = svc.restart or "none"
        ports_str = ", ".join(svc.ports) if svc.ports else "-"
        lines.append(f"| {svc.name} | {src} | {ports_str} | {restart} |")
    return "\n".join(lines)


def format_ports_text(services: List[ServiceInfo]) -> str:
    lines = []
    seen_host: Dict[str, List[str]] = {}
    for svc in services:
        for p in svc.ports:
            parts = p.split(":")
            host_port = parts[-2].split("/")[0] if len(parts) >= 2 else None
            if host_port:
                seen_host.setdefault(host_port, []).append(svc.name)
            lines.append(f"  {svc.name:<20} {p}")
    conflict_lines = []
    for hp, svcs in seen_host.items():
        if len(svcs) > 1:
            conflict_lines.append(f"  {_color('[CONFLICT]', 'error')} host port {hp} mapped by: {', '.join(svcs)}")
    if not lines:
        return "No port mappings found."
    result = "\n".join(lines)
    if conflict_lines:
        result += "\n\nPort Conflicts:\n" + "\n".join(conflict_lines)
    return result


def format_ports_json(services: List[ServiceInfo]) -> str:
    data = []
    seen_host: Dict[str, List[str]] = {}
    for svc in services:
        for p in svc.ports:
            parts = p.split(":")
            host_port = parts[-2].split("/")[0] if len(parts) >= 2 else None
            if host_port:
                seen_host.setdefault(host_port, []).append(svc.name)
            data.append({"service": svc.name, "mapping": p, "host_port": host_port})
    conflicts = [{"host_port": hp, "services": svcs} for hp, svcs in seen_host.items() if len(svcs) > 1]
    return json.dumps({"mappings": data, "conflicts": conflicts}, indent=2)


def format_ports_markdown(services: List[ServiceInfo]) -> str:
    lines = ["| Service | Port Mapping |",
             "|---------|-------------|"]
    for svc in services:
        for p in svc.ports:
            lines.append(f"| {svc.name} | `{p}` |")
    if len(lines) == 2:
        return "_No port mappings found._"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_lint(args) -> int:
    text = _read_file(args.file)
    nodes = parse_compose(text)
    issues = lint_compose(nodes, ignore_rules=args.ignore, min_severity=args.min_severity)

    fmt = args.format
    if fmt == "json":
        print(format_issues_json(issues))
    elif fmt == "markdown":
        print(format_issues_markdown(issues))
    else:
        counts = {"error": 0, "warning": 0, "info": 0}
        for iss in issues:
            counts[iss.severity] = counts.get(iss.severity, 0) + 1
        print(f"Linting: {args.file}")
        print(f"Found {len(issues)} issue(s): {counts['error']} errors, {counts['warning']} warnings, {counts['info']} info\n")
        print(format_issues_text(issues))

    if args.strict and issues:
        return 1
    errors = [i for i in issues if i.severity == "error"]
    return 1 if errors else 0


def cmd_services(args) -> int:
    text = _read_file(args.file)
    nodes = parse_compose(text)
    services = extract_services(nodes)

    fmt = args.format
    if fmt == "json":
        print(format_services_json(services))
    elif fmt == "markdown":
        print(format_services_markdown(services))
    else:
        print(f"Services in {args.file} ({len(services)} total):\n")
        print(format_services_text(services))
    return 0


def cmd_ports(args) -> int:
    text = _read_file(args.file)
    nodes = parse_compose(text)
    services = extract_services(nodes)

    fmt = args.format
    if fmt == "json":
        print(format_ports_json(services))
    elif fmt == "markdown":
        print(format_ports_markdown(services))
    else:
        print(f"Port mappings in {args.file}:\n")
        print(format_ports_text(services))
    return 0


def cmd_audit(args) -> int:
    text = _read_file(args.file)
    nodes = parse_compose(text)
    issues = lint_compose(nodes, ignore_rules=args.ignore, min_severity=args.min_severity)
    services = extract_services(nodes)

    fmt = args.format

    if fmt == "json":
        out = {
            "file": args.file,
            "issues": [i.to_dict() for i in issues],
            "services": [
                {"name": s.name, "image": s.image, "build": s.build,
                 "ports": s.ports, "restart": s.restart}
                for s in services
            ],
        }
        print(json.dumps(out, indent=2))
    elif fmt == "markdown":
        print(f"# docker-compose Audit: `{args.file}`\n")
        print("## Services\n")
        print(format_services_markdown(services))
        print("\n## Port Mappings\n")
        print(format_ports_markdown(services))
        print("\n## Lint Issues\n")
        print(format_issues_markdown(issues))
    else:
        counts = {"error": 0, "warning": 0, "info": 0}
        for iss in issues:
            counts[iss.severity] = counts.get(iss.severity, 0) + 1
        print(f"=== Audit: {args.file} ===\n")
        print(f"Services ({len(services)}):")
        print(format_services_text(services))
        print(f"\nPort Mappings:")
        print(format_ports_text(services))
        print(f"\nLint Issues ({len(issues)}: {counts['error']} errors, {counts['warning']} warnings, {counts['info']} info):")
        print(format_issues_text(issues))

    if args.strict and issues:
        return 1
    errors = [i for i in issues if i.severity == "error"]
    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except PermissionError:
        print(f"Error: permission denied: {path}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="docker-compose-linter",
        description="Lint docker-compose.yml files for security, best practices, and port conflicts.",
    )
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any issue (not just errors)")
    parser.add_argument("--ignore", metavar="RULE", action="append", default=[],
                        help="Ignore a specific rule (repeatable)")
    parser.add_argument("--min-severity", choices=["error", "warning", "info"], default="info",
                        dest="min_severity", help="Minimum severity to report (default: info)")

    sub = parser.add_subparsers(dest="command", required=True)

    lint_p = sub.add_parser("lint", help="Lint a docker-compose.yml for issues")
    lint_p.add_argument("file", metavar="FILE", help="Path to docker-compose.yml")

    svc_p = sub.add_parser("services", help="List all services with their images/builds")
    svc_p.add_argument("file", metavar="FILE", help="Path to docker-compose.yml")

    ports_p = sub.add_parser("ports", help="List all port mappings, detect conflicts")
    ports_p.add_argument("file", metavar="FILE", help="Path to docker-compose.yml")

    audit_p = sub.add_parser("audit", help="Full audit (lint + services + ports summary)")
    audit_p.add_argument("file", metavar="FILE", help="Path to docker-compose.yml")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "lint": cmd_lint,
        "services": cmd_services,
        "ports": cmd_ports,
        "audit": cmd_audit,
    }

    handler = dispatch.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(1)

    sys.exit(handler(args))


if __name__ == "__main__":
    main()
