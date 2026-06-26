#!/usr/bin/env python3
"""Dependency vulnerability scanner for npm, pip, and Go projects.

Scans project dependency files (package.json, requirements.txt, go.mod) and checks
for known vulnerabilities using the OSV.dev API (free, no API key required).
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error


def parse_package_json(path):
    """Parse package.json for dependencies."""
    with open(path, "r") as f:
        data = json.load(f)
    deps = {}
    for section in ("dependencies", "devDependencies"):
        if section in data:
            for name, ver in data[section].items():
                # Strip leading ^, ~, >=, etc. to get base version
                clean = re.sub(r"^[\^~>=<]*", "", ver).strip()
                if clean and re.match(r"\d", clean):
                    deps[name] = clean
    return deps, "npm"


def parse_requirements_txt(path):
    """Parse requirements.txt for dependencies."""
    deps = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Handle ==, >=, <=, ~=, !=
            match = re.match(r"^([a-zA-Z0-9_.-]+)\s*[=~!<>]=?\s*([0-9][0-9a-zA-Z.*-]*)", line)
            if match:
                deps[match.group(1)] = match.group(2)
            else:
                # Package without version
                name_match = re.match(r"^([a-zA-Z0-9_.-]+)", line)
                if name_match:
                    deps[name_match.group(1)] = ""
    return deps, "PyPI"


def parse_go_mod(path):
    """Parse go.mod for dependencies."""
    deps = {}
    in_require = False
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("require ("):
                in_require = True
                continue
            if in_require and line == ")":
                in_require = False
                continue
            if line.startswith("require "):
                parts = line.split()
                if len(parts) >= 3:
                    deps[parts[1]] = parts[2].lstrip("v")
            elif in_require:
                parts = line.split()
                if len(parts) >= 2 and not parts[0].startswith("//"):
                    deps[parts[0]] = parts[1].lstrip("v")
    return deps, "Go"


def detect_project(directory):
    """Auto-detect project type from files in directory."""
    results = []
    for fname, parser in [
        ("package.json", parse_package_json),
        ("requirements.txt", parse_requirements_txt),
        ("go.mod", parse_go_mod),
    ]:
        fpath = os.path.join(directory, fname)
        if os.path.isfile(fpath):
            results.append((fpath, parser))
    return results


def query_osv(package_name, version, ecosystem):
    """Query OSV.dev API for vulnerabilities."""
    url = "https://api.osv.dev/v1/query"
    payload = {
        "package": {"name": package_name, "ecosystem": ecosystem},
    }
    if version:
        payload["version"] = version

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("vulns", [])
    except urllib.error.HTTPError:
        return []
    except urllib.error.URLError:
        return []
    except Exception:
        return []


def severity_color(severity):
    """Return ANSI color for severity."""
    colors = {
        "CRITICAL": "\033[91m",  # Red
        "HIGH": "\033[91m",      # Red
        "MODERATE": "\033[93m",  # Yellow
        "MEDIUM": "\033[93m",    # Yellow
        "LOW": "\033[92m",       # Green
    }
    return colors.get(severity.upper(), "\033[0m")


RESET = "\033[0m"


def extract_severity(vuln):
    """Extract severity from a vulnerability entry."""
    severity = "UNKNOWN"
    if "database_specific" in vuln and "severity" in vuln["database_specific"]:
        severity = vuln["database_specific"]["severity"]
    elif "severity" in vuln:
        for s in vuln["severity"]:
            if s.get("type") == "CVSS_V3":
                score_match = re.search(r"CVSS:\d\.\d/AV:\w", s.get("score", ""))
                if not score_match:
                    # Try to parse numeric score
                    try:
                        score_val = float(s.get("score", "0"))
                        if score_val >= 9.0:
                            severity = "CRITICAL"
                        elif score_val >= 7.0:
                            severity = "HIGH"
                        elif score_val >= 4.0:
                            severity = "MEDIUM"
                        else:
                            severity = "LOW"
                    except (ValueError, TypeError):
                        pass
    return severity


def scan(directory, output_json=False, ecosystems=None):
    """Main scan routine."""
    projects = detect_project(directory)
    if not projects:
        print(f"No supported dependency files found in: {directory}")
        print("Supported: package.json, requirements.txt, go.mod")
        sys.exit(1)

    all_findings = []

    for fpath, parser in projects:
        deps, ecosystem = parser(fpath)

        if ecosystems and ecosystem.lower() not in [e.lower() for e in ecosystems]:
            continue

        print(f"\n{'='*60}")
        print(f"Scanning: {os.path.basename(fpath)} ({ecosystem})")
        print(f"Found {len(deps)} dependencies")
        print(f"{'='*60}\n")

        vuln_count = 0
        for pkg_name, version in sorted(deps.items()):
            vulns = query_osv(pkg_name, version, ecosystem)
            if vulns:
                vuln_count += len(vulns)
                for v in vulns:
                    vuln_id = v.get("id", "N/A")
                    summary = v.get("summary", "No description")
                    severity = extract_severity(v)
                    aliases = v.get("aliases", [])
                    alias_str = ", ".join(aliases[:3]) if aliases else ""

                    finding = {
                        "package": pkg_name,
                        "version": version or "unspecified",
                        "ecosystem": ecosystem,
                        "vuln_id": vuln_id,
                        "severity": severity,
                        "summary": summary,
                        "aliases": aliases,
                    }
                    all_findings.append(finding)

                    if not output_json:
                        color = severity_color(severity)
                        print(f"  {color}[{severity}]{RESET} {pkg_name}@{version or '?'}")
                        print(f"    ID: {vuln_id}")
                        if alias_str:
                            print(f"    Aliases: {alias_str}")
                        print(f"    {summary[:120]}")
                        print()

        if not output_json:
            if vuln_count == 0:
                print(f"  \033[92mNo vulnerabilities found!\033[0m\n")
            else:
                print(f"  Total: {vuln_count} vulnerability(ies) found\n")

    if output_json:
        print(json.dumps(all_findings, indent=2))
    else:
        total = len(all_findings)
        critical = sum(1 for f in all_findings if f["severity"] in ("CRITICAL", "HIGH"))
        print(f"{'='*60}")
        print(f"SUMMARY: {total} vulnerabilities ({critical} critical/high)")
        print(f"{'='*60}")

    return len(all_findings)


def main():
    parser = argparse.ArgumentParser(
        description="Scan project dependencies for known vulnerabilities using OSV.dev",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .                        Scan current directory
  %(prog)s /path/to/project         Scan specific project
  %(prog)s . --json                 Output as JSON
  %(prog)s . --ecosystem npm        Scan only npm dependencies
  %(prog)s . --ecosystem PyPI       Scan only Python dependencies

Supported dependency files:
  - package.json (npm)
  - requirements.txt (PyPI/pip)
  - go.mod (Go)
        """,
    )
    parser.add_argument("directory", nargs="?", default=".", help="Project directory to scan (default: .)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--ecosystem", action="append", help="Filter by ecosystem (npm, PyPI, Go). Repeatable.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory")
        sys.exit(1)

    vuln_count = scan(args.directory, output_json=args.json, ecosystems=args.ecosystem)
    sys.exit(1 if vuln_count > 0 else 0)


if __name__ == "__main__":
    main()
