#!/usr/bin/env python3
"""Runbook Generator — create operational runbooks from project infrastructure files.

Scans Dockerfiles, docker-compose.yml, systemd units, Makefiles, package.json,
.env files, and nginx configs to produce step-by-step operational runbooks.

Pure Python stdlib — no external dependencies.

Usage:
    python3 generate_runbook.py /path/to/project
    python3 generate_runbook.py /path/to/project --format json
    python3 generate_runbook.py /path/to/project -o RUNBOOK.md
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path


# ── Scanners ────────────────────────────────────────────────────────────────

def scan_dockerfile(path):
    """Extract operational info from Dockerfile."""
    info = {
        "type": "dockerfile",
        "path": str(path),
        "base_image": None,
        "exposed_ports": [],
        "env_vars": {},
        "entrypoint": None,
        "cmd": None,
        "workdir": None,
        "build_stages": [],
        "health_check": None,
    }

    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return info

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        directive, args = parts[0].upper(), parts[1]

        if directive == "FROM":
            # Handle multi-stage builds
            image = args.split(" AS ")[0].strip() if " AS " in args.upper() else args.strip()
            if not info["base_image"]:
                info["base_image"] = image
            stage = args.split(" AS ")[-1].strip() if " AS " in args.upper() else None
            if stage:
                info["build_stages"].append(stage)
        elif directive == "EXPOSE":
            info["exposed_ports"].extend(re.findall(r'\d+', args))
        elif directive == "ENV":
            match = re.match(r'(\w+)[= ](.+)', args)
            if match:
                info["env_vars"][match.group(1)] = match.group(2).strip()
        elif directive == "ENTRYPOINT":
            info["entrypoint"] = args
        elif directive == "CMD":
            info["cmd"] = args
        elif directive == "WORKDIR":
            info["workdir"] = args
        elif directive == "HEALTHCHECK":
            info["health_check"] = args

    return info


def scan_docker_compose(path):
    """Extract service info from docker-compose.yml (basic YAML parsing)."""
    info = {
        "type": "docker_compose",
        "path": str(path),
        "services": {},
    }

    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return info

    # Basic YAML parsing for docker-compose (handles common cases)
    current_service = None
    current_section = None
    indent_level = 0

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        # Top-level keys
        if indent == 0 and stripped.endswith(":"):
            current_section = stripped[:-1]
            current_service = None
            continue

        # Service names (under services:)
        if current_section == "services" and indent == 2 and stripped.endswith(":"):
            current_service = stripped[:-1]
            info["services"][current_service] = {
                "image": None,
                "build": None,
                "ports": [],
                "volumes": [],
                "environment": [],
                "depends_on": [],
                "restart": None,
                "command": None,
                "healthcheck": None,
            }
            continue

        if not current_service or current_section != "services":
            continue

        svc = info["services"][current_service]

        # Service properties
        if "image:" in stripped:
            svc["image"] = stripped.split("image:", 1)[1].strip()
        elif "build:" in stripped and not stripped.startswith("-"):
            svc["build"] = stripped.split("build:", 1)[1].strip() or "."
        elif "restart:" in stripped:
            svc["restart"] = stripped.split("restart:", 1)[1].strip()
        elif "command:" in stripped:
            svc["command"] = stripped.split("command:", 1)[1].strip()
        elif stripped.startswith("- ") and indent >= 4:
            val = stripped[2:].strip().strip('"').strip("'")
            # Determine which list we're in based on context
            # Look at previous non-list lines
            if "ports:" in content.splitlines()[max(0, content.splitlines().index(line) - 5):content.splitlines().index(line)][-1] if content.splitlines().index(line) > 0 else "":
                pass
            # Simple heuristic: if it looks like a port mapping
            if re.match(r'"\d+:\d+"|\d+:\d+', val):
                svc["ports"].append(val)
            elif re.match(r'[./].*:.*', val):
                svc["volumes"].append(val)
            elif "=" in val:
                svc["environment"].append(val)
        elif "depends_on:" in stripped:
            pass  # deps will be on next lines

    return info


def scan_systemd_unit(path):
    """Extract operational info from systemd unit file."""
    info = {
        "type": "systemd",
        "path": str(path),
        "description": None,
        "exec_start": None,
        "exec_stop": None,
        "exec_reload": None,
        "working_dir": None,
        "user": None,
        "restart_policy": None,
        "after": [],
        "requires": [],
        "environment": [],
        "env_file": None,
    }

    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return info

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("["):
            continue

        if "=" not in line:
            continue

        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()

        mapping = {
            "Description": "description",
            "ExecStart": "exec_start",
            "ExecStop": "exec_stop",
            "ExecReload": "exec_reload",
            "WorkingDirectory": "working_dir",
            "User": "user",
            "Restart": "restart_policy",
            "EnvironmentFile": "env_file",
        }

        if key in mapping:
            info[mapping[key]] = val
        elif key == "After":
            info["after"].extend(val.split())
        elif key == "Requires":
            info["requires"].extend(val.split())
        elif key == "Environment":
            info["environment"].append(val)

    return info


def scan_makefile(path):
    """Extract targets from Makefile."""
    info = {
        "type": "makefile",
        "path": str(path),
        "targets": {},
    }

    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return info

    current_target = None
    for line in content.splitlines():
        # Target definition
        match = re.match(r'^([a-zA-Z_][\w-]*)\s*:', line)
        if match and not line.startswith("\t"):
            current_target = match.group(1)
            # Check for preceding comment
            info["targets"][current_target] = {
                "commands": [],
                "phony": False,
            }
            continue

        if line.startswith("\t") and current_target:
            cmd = line.strip()
            if cmd and not cmd.startswith("#"):
                info["targets"][current_target]["commands"].append(cmd)

        if ".PHONY:" in line:
            phonies = line.split(".PHONY:", 1)[1].strip().split()
            for p in phonies:
                if p in info["targets"]:
                    info["targets"][p]["phony"] = True

    return info


def scan_package_json(path):
    """Extract scripts and metadata from package.json."""
    info = {
        "type": "package_json",
        "path": str(path),
        "name": None,
        "version": None,
        "scripts": {},
        "engines": {},
    }

    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return info

    info["name"] = data.get("name")
    info["version"] = data.get("version")
    info["scripts"] = data.get("scripts", {})
    info["engines"] = data.get("engines", {})

    return info


def scan_env_file(path):
    """Extract environment variables from .env or .env.example."""
    info = {
        "type": "env_file",
        "path": str(path),
        "variables": {},
    }

    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return info

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.*)', line)
        if match:
            key = match.group(1)
            val = match.group(2).strip().strip('"').strip("'")
            # Mask actual values, keep examples
            if path.name == ".env.example" or not val or val.startswith("$") or val in ("true", "false"):
                info["variables"][key] = val
            else:
                info["variables"][key] = "<set in .env>"

    return info


def scan_nginx_conf(path):
    """Extract basic info from nginx config."""
    info = {
        "type": "nginx",
        "path": str(path),
        "listen_ports": [],
        "server_names": [],
        "upstreams": [],
        "locations": [],
    }

    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return info

    for line in content.splitlines():
        line = line.strip().rstrip(";")
        if line.startswith("listen"):
            port = re.findall(r'\d+', line)
            if port:
                info["listen_ports"].extend(port)
        elif line.startswith("server_name"):
            names = line.split()[1:]
            info["server_names"].extend(names)
        elif line.startswith("upstream"):
            name = line.split()[1] if len(line.split()) > 1 else "unknown"
            info["upstreams"].append(name)
        elif line.startswith("location"):
            loc = line.split(None, 1)[1] if len(line.split()) > 1 else "/"
            info["locations"].append(loc.rstrip("{").strip())

    return info


# ── Project Scanner ─────────────────────────────────────────────────────────

SCAN_TARGETS = {
    "Dockerfile": scan_dockerfile,
    "docker-compose.yml": scan_docker_compose,
    "docker-compose.yaml": scan_docker_compose,
    "Makefile": scan_makefile,
    "package.json": scan_package_json,
    ".env.example": scan_env_file,
    ".env.sample": scan_env_file,
    "nginx.conf": scan_nginx_conf,
}

SYSTEMD_GLOB = "*.service"
NGINX_GLOB = "*.conf"


def scan_project(project_path):
    """Scan a project directory for infrastructure files."""
    root = Path(project_path)
    if not root.is_dir():
        print(f"Error: {project_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    scanned = []

    # Scan known files
    for filename, scanner in SCAN_TARGETS.items():
        filepath = root / filename
        if filepath.exists():
            scanned.append(scanner(filepath))

    # Scan for systemd units
    for f in root.rglob(SYSTEMD_GLOB):
        if f.is_file() and "[Unit]" in f.read_text()[:200]:
            scanned.append(scan_systemd_unit(f))

    # Scan for .env (not .example)
    env_file = root / ".env"
    if env_file.exists():
        scanned.append(scan_env_file(env_file))

    # Scan for nginx configs in common locations
    for nginx_dir in ["nginx", "conf", "config"]:
        nginx_path = root / nginx_dir
        if nginx_path.is_dir():
            for f in nginx_path.glob("*.conf"):
                scanned.append(scan_nginx_conf(f))

    return scanned


# ── Runbook Generator ───────────────────────────────────────────────────────

def generate_runbook(project_path, scanned):
    """Generate a Markdown runbook from scanned data."""
    root = Path(project_path)
    project_name = root.name

    # Determine project type and collect info
    has_docker = any(s["type"] == "dockerfile" for s in scanned)
    has_compose = any(s["type"] == "docker_compose" for s in scanned)
    has_systemd = any(s["type"] == "systemd" for s in scanned)
    has_makefile = any(s["type"] == "makefile" for s in scanned)
    has_npm = any(s["type"] == "package_json" for s in scanned)
    has_nginx = any(s["type"] == "nginx" for s in scanned)

    # Collect all env vars
    all_env = {}
    for s in scanned:
        if s["type"] == "env_file":
            all_env.update(s.get("variables", {}))
        elif s["type"] == "dockerfile":
            all_env.update(s.get("env_vars", {}))

    # Collect all ports
    all_ports = set()
    for s in scanned:
        if s["type"] == "dockerfile":
            all_ports.update(s.get("exposed_ports", []))
        elif s["type"] == "nginx":
            all_ports.update(s.get("listen_ports", []))

    # Determine tech stack
    tech_stack = []
    for s in scanned:
        if s["type"] == "dockerfile" and s.get("base_image"):
            tech_stack.append(s["base_image"])
        if s["type"] == "package_json" and s.get("name"):
            tech_stack.append("Node.js")

    lines = []

    # ── 1. Overview ──
    lines.append(f"# {project_name} — Operational Runbook")
    lines.append("")
    lines.append(f"**Project:** {project_name}")
    lines.append(f"**Path:** `{root.resolve()}`")
    if tech_stack:
        lines.append(f"**Stack:** {', '.join(tech_stack)}")
    if all_ports:
        lines.append(f"**Ports:** {', '.join(sorted(all_ports))}")
    lines.append(f"**Generated:** Auto-generated runbook — review and customize before use")
    lines.append("")

    # ── 2. Prerequisites ──
    lines.append("## Prerequisites")
    lines.append("")
    prereqs = []
    if has_docker or has_compose:
        prereqs.append("- Docker Engine installed and running")
    if has_compose:
        prereqs.append("- Docker Compose v2+")
    if has_npm:
        for s in scanned:
            if s["type"] == "package_json" and s.get("engines"):
                for engine, ver in s["engines"].items():
                    prereqs.append(f"- {engine} {ver}")
        if not any("Node" in p for p in prereqs):
            prereqs.append("- Node.js + npm")
    if has_makefile:
        prereqs.append("- GNU Make")
    if has_systemd:
        prereqs.append("- systemd-based Linux system")
    if not prereqs:
        prereqs.append("- (No specific prerequisites detected)")
    lines.extend(prereqs)
    lines.append("")

    # ── 3. Environment Variables ──
    if all_env:
        lines.append("## Environment Variables")
        lines.append("")
        lines.append("```bash")
        lines.append("# Copy .env.example to .env and fill in values")
        lines.append("cp .env.example .env")
        lines.append("```")
        lines.append("")
        lines.append("| Variable | Default/Example | Required |")
        lines.append("|----------|----------------|----------|")
        for key, val in sorted(all_env.items()):
            required = "Yes" if not val or val == "<set in .env>" else "No"
            display_val = val if val else "(empty)"
            lines.append(f"| `{key}` | `{display_val}` | {required} |")
        lines.append("")

    # ── 4. Build ──
    lines.append("## Build")
    lines.append("")

    if has_docker:
        for s in scanned:
            if s["type"] == "dockerfile":
                lines.append("### Docker Build")
                lines.append("")
                lines.append("```bash")
                if s.get("build_stages"):
                    lines.append(f"# Multi-stage build (stages: {', '.join(s['build_stages'])})")
                lines.append(f"docker build -t {project_name}:latest .")
                lines.append("```")
                lines.append("")

    if has_compose:
        lines.append("### Docker Compose Build")
        lines.append("")
        lines.append("```bash")
        lines.append("docker compose build")
        lines.append("```")
        lines.append("")

    if has_npm:
        for s in scanned:
            if s["type"] == "package_json" and s.get("scripts"):
                scripts = s["scripts"]
                if "build" in scripts:
                    lines.append("### npm Build")
                    lines.append("")
                    lines.append("```bash")
                    lines.append("npm install")
                    lines.append("npm run build")
                    lines.append("```")
                    lines.append("")

    if has_makefile:
        for s in scanned:
            if s["type"] == "makefile":
                if "build" in s["targets"]:
                    lines.append("### Make Build")
                    lines.append("")
                    lines.append("```bash")
                    lines.append("make build")
                    lines.append("```")
                    lines.append("")

    # ── 5. Deploy ──
    lines.append("## Deploy")
    lines.append("")

    if has_compose:
        lines.append("### Docker Compose Deploy")
        lines.append("")
        lines.append("```bash")
        lines.append("# Pull latest images and start")
        lines.append("docker compose pull")
        lines.append("docker compose up -d")
        lines.append("")
        lines.append("# Verify")
        lines.append("docker compose ps")
        lines.append("```")
        lines.append("")
    elif has_docker:
        lines.append("### Docker Deploy")
        lines.append("")
        lines.append("```bash")
        lines.append(f"docker run -d --name {project_name} \\")
        port_flags = " ".join(f"-p {p}:{p}" for p in sorted(all_ports)) if all_ports else "-p 8080:8080"
        lines.append(f"  {port_flags} \\")
        lines.append(f"  --restart unless-stopped \\")
        lines.append(f"  {project_name}:latest")
        lines.append("```")
        lines.append("")

    if has_systemd:
        for s in scanned:
            if s["type"] == "systemd":
                unit_name = Path(s["path"]).name
                lines.append(f"### systemd Deploy ({unit_name})")
                lines.append("")
                lines.append("```bash")
                lines.append(f"sudo cp {s['path']} /etc/systemd/system/")
                lines.append("sudo systemctl daemon-reload")
                lines.append(f"sudo systemctl enable {unit_name}")
                lines.append(f"sudo systemctl start {unit_name}")
                lines.append("```")
                lines.append("")

    if has_makefile:
        for s in scanned:
            if s["type"] == "makefile" and "deploy" in s["targets"]:
                lines.append("### Make Deploy")
                lines.append("")
                lines.append("```bash")
                lines.append("make deploy")
                lines.append("```")
                lines.append("")

    # ── 6. Start / Stop / Restart ──
    lines.append("## Start / Stop / Restart")
    lines.append("")

    if has_compose:
        lines.append("```bash")
        lines.append("# Start")
        lines.append("docker compose up -d")
        lines.append("")
        lines.append("# Stop")
        lines.append("docker compose down")
        lines.append("")
        lines.append("# Restart")
        lines.append("docker compose restart")
        lines.append("")
        lines.append("# Restart single service")
        for s in scanned:
            if s["type"] == "docker_compose":
                for svc_name in list(s.get("services", {}).keys())[:3]:
                    lines.append(f"docker compose restart {svc_name}")
        lines.append("```")
        lines.append("")
    elif has_docker:
        lines.append("```bash")
        lines.append(f"docker start {project_name}")
        lines.append(f"docker stop {project_name}")
        lines.append(f"docker restart {project_name}")
        lines.append("```")
        lines.append("")

    if has_systemd:
        for s in scanned:
            if s["type"] == "systemd":
                unit = Path(s["path"]).name
                lines.append(f"### systemd ({unit})")
                lines.append("")
                lines.append("```bash")
                lines.append(f"sudo systemctl start {unit}")
                lines.append(f"sudo systemctl stop {unit}")
                lines.append(f"sudo systemctl restart {unit}")
                if s.get("exec_reload"):
                    lines.append(f"sudo systemctl reload {unit}  # {s['exec_reload']}")
                lines.append(f"sudo systemctl status {unit}")
                lines.append("```")
                lines.append("")

    if has_npm:
        for s in scanned:
            if s["type"] == "package_json" and "start" in s.get("scripts", {}):
                lines.append("### npm")
                lines.append("")
                lines.append("```bash")
                lines.append("npm start")
                if "dev" in s["scripts"]:
                    lines.append("npm run dev  # development mode")
                lines.append("```")
                lines.append("")

    # ── 7. Health Check ──
    lines.append("## Health Check")
    lines.append("")

    health_checks = []
    if has_compose:
        health_checks.append("docker compose ps")
    elif has_docker:
        health_checks.append(f"docker ps --filter name={project_name}")
    if has_systemd:
        for s in scanned:
            if s["type"] == "systemd":
                health_checks.append(f"sudo systemctl status {Path(s['path']).name}")
    if all_ports:
        for port in sorted(all_ports)[:3]:
            health_checks.append(f"curl -sf http://localhost:{port}/ && echo 'OK' || echo 'FAIL'")

    if health_checks:
        lines.append("```bash")
        for hc in health_checks:
            lines.append(hc)
        lines.append("```")
    else:
        lines.append("```bash")
        lines.append("# Add health check commands here")
        lines.append("curl -sf http://localhost:8080/health && echo 'OK' || echo 'FAIL'")
        lines.append("```")
    lines.append("")

    # ── 8. Rollback ──
    lines.append("## Rollback")
    lines.append("")

    if has_compose or has_docker:
        lines.append("```bash")
        lines.append("# Tag current as backup before deploy")
        lines.append(f"docker tag {project_name}:latest {project_name}:rollback")
        lines.append("")
        lines.append("# Rollback")
        if has_compose:
            lines.append("docker compose down")
            lines.append(f"# Edit docker-compose.yml to use previous image tag")
            lines.append("docker compose up -d")
        else:
            lines.append(f"docker stop {project_name}")
            lines.append(f"docker rm {project_name}")
            lines.append(f"docker run -d --name {project_name} {project_name}:rollback")
        lines.append("```")
    else:
        lines.append("```bash")
        lines.append("# Manual rollback procedure:")
        lines.append("# 1. Identify the last known good version/commit")
        lines.append("# 2. git checkout <commit>")
        lines.append("# 3. Rebuild and redeploy")
        lines.append("```")
    lines.append("")

    # ── 9. Troubleshooting ──
    lines.append("## Troubleshooting")
    lines.append("")
    lines.append("### View Logs")
    lines.append("")
    lines.append("```bash")

    if has_compose:
        lines.append("# All services")
        lines.append("docker compose logs -f")
        lines.append("")
        lines.append("# Single service")
        for s in scanned:
            if s["type"] == "docker_compose":
                for svc_name in list(s.get("services", {}).keys())[:2]:
                    lines.append(f"docker compose logs -f {svc_name}")
                break
    elif has_docker:
        lines.append(f"docker logs -f {project_name}")

    if has_systemd:
        for s in scanned:
            if s["type"] == "systemd":
                unit = Path(s["path"]).name
                lines.append(f"journalctl -u {unit} -f")

    lines.append("```")
    lines.append("")

    lines.append("### Common Issues")
    lines.append("")
    lines.append("| Symptom | Possible Cause | Fix |")
    lines.append("|---------|---------------|-----|")
    if all_ports:
        port = sorted(all_ports)[0]
        lines.append(f"| Port {port} already in use | Another process on port | `lsof -i :{port}` to find and stop it |")
    lines.append("| Container won't start | Missing env vars | Check `.env` file has all required vars |")
    if has_docker:
        lines.append("| Build fails | Cached layers stale | `docker build --no-cache -t name .` |")
    lines.append("| OOM killed | Memory limit too low | Increase container memory or optimize app |")
    lines.append("| Permission denied | File ownership | Check user/group in Dockerfile or systemd |")
    lines.append("")

    # ── 10. Monitoring ──
    lines.append("## Monitoring")
    lines.append("")
    lines.append("### Logs Location")
    lines.append("")
    if has_docker or has_compose:
        lines.append("- Docker: `docker logs <container>`")
    if has_systemd:
        lines.append("- systemd: `journalctl -u <unit>`")
    if has_nginx:
        lines.append("- Nginx: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`")
    lines.append("- Application: Check app config for log file paths")
    lines.append("")

    # ── 11. Contacts ──
    lines.append("## Contacts")
    lines.append("")
    lines.append("| Role | Name | Contact |")
    lines.append("|------|------|---------|")
    lines.append("| Primary On-Call | (fill in) | (fill in) |")
    lines.append("| Secondary On-Call | (fill in) | (fill in) |")
    lines.append("| Team Lead | (fill in) | (fill in) |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*This runbook was auto-generated. Review all commands before executing in production.*")

    return "\n".join(lines)


def generate_json(project_path, scanned):
    """Generate JSON structured runbook data."""
    return json.dumps({
        "project": Path(project_path).name,
        "path": str(Path(project_path).resolve()),
        "sources": scanned,
        "summary": {
            "has_docker": any(s["type"] == "dockerfile" for s in scanned),
            "has_compose": any(s["type"] == "docker_compose" for s in scanned),
            "has_systemd": any(s["type"] == "systemd" for s in scanned),
            "has_npm": any(s["type"] == "package_json" for s in scanned),
            "has_makefile": any(s["type"] == "makefile" for s in scanned),
            "has_nginx": any(s["type"] == "nginx" for s in scanned),
            "files_scanned": len(scanned),
        },
    }, indent=2)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Runbook Generator — create operational runbooks from project infrastructure files"
    )
    parser.add_argument("project_path", help="Path to project directory to scan")
    parser.add_argument("--format", "-f", choices=["markdown", "json"],
                       default="markdown", help="Output format (default: markdown)")
    parser.add_argument("-o", "--output", help="Write output to file instead of stdout")

    args = parser.parse_args()

    scanned = scan_project(args.project_path)

    if not scanned:
        print(f"No infrastructure files found in {args.project_path}", file=sys.stderr)
        print("Looked for: Dockerfile, docker-compose.yml, *.service, Makefile, package.json, .env", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        output = generate_json(args.project_path, scanned)
    else:
        output = generate_runbook(args.project_path, scanned)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Runbook written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
