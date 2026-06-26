#!/usr/bin/env python3
"""Dependency graph analyzer for projects.

Supports: Python (requirements.txt, pyproject.toml, setup.py/cfg),
Node.js (package.json), Go (go.mod), Rust (Cargo.toml).

Outputs a tree view or JSON of project dependencies.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict


def detect_project_type(path):
    """Detect project type from manifest files present."""
    detected = []
    files = os.listdir(path) if os.path.isdir(path) else []
    if "package.json" in files:
        detected.append("node")
    if "requirements.txt" in files:
        detected.append("python-req")
    if "pyproject.toml" in files:
        detected.append("python-pyproject")
    if "setup.py" in files or "setup.cfg" in files:
        detected.append("python-setup")
    if "go.mod" in files:
        detected.append("go")
    if "Cargo.toml" in files:
        detected.append("rust")
    if "Gemfile" in files:
        detected.append("ruby")
    if "composer.json" in files:
        detected.append("php")
    return detected


def parse_requirements_txt(filepath):
    """Parse Python requirements.txt."""
    deps = {"production": [], "dev": []}
    if not os.path.isfile(filepath):
        return deps
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Handle -r includes
            match = re.match(r'^([A-Za-z0-9_][A-Za-z0-9._-]*)\s*([>=<!~].*)?', line)
            if match:
                name = match.group(1).lower()
                version = (match.group(2) or "").strip()
                deps["production"].append({"name": name, "version": version or "*"})
    return deps


def parse_package_json(filepath):
    """Parse Node.js package.json."""
    deps = {"production": [], "dev": [], "peer": []}
    if not os.path.isfile(filepath):
        return deps
    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return deps

    for name, version in data.get("dependencies", {}).items():
        deps["production"].append({"name": name, "version": version})
    for name, version in data.get("devDependencies", {}).items():
        deps["dev"].append({"name": name, "version": version})
    for name, version in data.get("peerDependencies", {}).items():
        deps["peer"].append({"name": name, "version": version})
    return deps


def parse_go_mod(filepath):
    """Parse Go go.mod."""
    deps = {"production": [], "dev": []}
    if not os.path.isfile(filepath):
        return deps
    in_require = False
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("require ("):
                in_require = True
                continue
            if in_require and line == ")":
                in_require = False
                continue
            if in_require:
                # module v1.2.3
                match = re.match(r'^(\S+)\s+(\S+)', line)
                if match:
                    indirect = "// indirect" in line
                    dep_type = "dev" if indirect else "production"
                    deps[dep_type].append({"name": match.group(1), "version": match.group(2)})
            elif line.startswith("require "):
                match = re.match(r'^require\s+(\S+)\s+(\S+)', line)
                if match:
                    deps["production"].append({"name": match.group(1), "version": match.group(2)})
    return deps


def parse_cargo_toml(filepath):
    """Parse Rust Cargo.toml (basic parser, no full TOML lib needed)."""
    deps = {"production": [], "dev": []}
    if not os.path.isfile(filepath):
        return deps
    section = None
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("["):
                section = line.strip("[]").strip().lower()
                continue
            if section in ("dependencies", "dev-dependencies") and "=" in line:
                parts = line.split("=", 1)
                name = parts[0].strip()
                value = parts[1].strip().strip('"').strip("'")
                dep_type = "dev" if section == "dev-dependencies" else "production"
                # Handle inline table: { version = "1.0", features = [...] }
                if value.startswith("{"):
                    vm = re.search(r'version\s*=\s*"([^"]*)"', value)
                    version = vm.group(1) if vm else "*"
                else:
                    version = value
                deps[dep_type].append({"name": name, "version": version})
    return deps


def parse_pyproject_toml(filepath):
    """Parse pyproject.toml for dependencies (basic parser)."""
    deps = {"production": [], "dev": []}
    if not os.path.isfile(filepath):
        return deps
    section = None
    with open(filepath, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("["):
                section = stripped.strip("[]").strip().lower()
                continue
            if section == "project" and stripped.startswith("dependencies"):
                # Try to parse inline array
                match = re.search(r'\[(.+)\]', stripped)
                if match:
                    items = match.group(1).split(",")
                    for item in items:
                        item = item.strip().strip('"').strip("'")
                        if item:
                            pm = re.match(r'^([A-Za-z0-9_][A-Za-z0-9._-]*)\s*(.*)', item)
                            if pm:
                                deps["production"].append({"name": pm.group(1).lower(), "version": pm.group(2).strip() or "*"})
            # Multi-line dependencies array
            if section == "project" and stripped.startswith('"') and not stripped.startswith('[['):
                item = stripped.strip('",').strip("',")
                if item:
                    pm = re.match(r'^([A-Za-z0-9_][A-Za-z0-9._-]*)\s*(.*)', item)
                    if pm:
                        deps["production"].append({"name": pm.group(1).lower(), "version": pm.group(2).strip() or "*"})
    return deps


def parse_gemfile(filepath):
    """Parse Ruby Gemfile (basic)."""
    deps = {"production": [], "dev": []}
    if not os.path.isfile(filepath):
        return deps
    in_group = None
    with open(filepath, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("group"):
                if "development" in stripped or "test" in stripped:
                    in_group = "dev"
                else:
                    in_group = "production"
                continue
            if stripped == "end":
                in_group = None
                continue
            match = re.match(r"gem\s+['\"]([^'\"]+)['\"](?:\s*,\s*['\"]([^'\"]+)['\"])?", stripped)
            if match:
                name = match.group(1)
                version = match.group(2) or "*"
                dep_type = in_group or "production"
                deps[dep_type].append({"name": name, "version": version})
    return deps


def parse_composer_json(filepath):
    """Parse PHP composer.json."""
    deps = {"production": [], "dev": []}
    if not os.path.isfile(filepath):
        return deps
    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return deps
    for name, version in data.get("require", {}).items():
        if name != "php":
            deps["production"].append({"name": name, "version": version})
    for name, version in data.get("require-dev", {}).items():
        deps["dev"].append({"name": name, "version": version})
    return deps


PARSERS = {
    "node": ("package.json", parse_package_json),
    "python-req": ("requirements.txt", parse_requirements_txt),
    "python-pyproject": ("pyproject.toml", parse_pyproject_toml),
    "go": ("go.mod", parse_go_mod),
    "rust": ("Cargo.toml", parse_cargo_toml),
    "ruby": ("Gemfile", parse_gemfile),
    "php": ("composer.json", parse_composer_json),
}


def format_tree(project_type, deps, show_versions=True):
    """Format dependencies as a tree."""
    lines = [f"📦 Project type: {project_type}"]
    total = sum(len(v) for v in deps.values())
    lines.append(f"   Total dependencies: {total}")
    lines.append("")

    for group, dep_list in deps.items():
        if not dep_list:
            continue
        icon = {"production": "├── 🔧", "dev": "├── 🧪", "peer": "├── 🔗"}.get(group, "├──")
        lines.append(f"{icon} {group} ({len(dep_list)})")
        for i, dep in enumerate(sorted(dep_list, key=lambda d: d["name"])):
            prefix = "│   ├──" if i < len(dep_list) - 1 else "│   └──"
            ver = f" @ {dep['version']}" if show_versions and dep.get("version") else ""
            lines.append(f"{prefix} {dep['name']}{ver}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze project dependencies. Supports Node.js, Python, Go, Rust, Ruby, PHP."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to project directory (default: current dir)",
    )
    parser.add_argument("--type", choices=list(PARSERS.keys()), help="Force project type")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-versions", action="store_true", help="Hide version constraints")
    parser.add_argument("--summary", action="store_true", help="Show only counts, not full tree")
    args = parser.parse_args()

    project_path = os.path.abspath(args.path)
    if not os.path.isdir(project_path):
        print(f"Error: '{project_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    if args.type:
        types_to_check = [args.type]
    else:
        types_to_check = detect_project_type(project_path)

    if not types_to_check:
        print(f"No supported manifest files found in: {project_path}", file=sys.stderr)
        print("Supported: package.json, requirements.txt, pyproject.toml, go.mod, Cargo.toml, Gemfile, composer.json", file=sys.stderr)
        sys.exit(1)

    all_results = {}
    for ptype in types_to_check:
        filename, parse_fn = PARSERS[ptype]
        filepath = os.path.join(project_path, filename)
        deps = parse_fn(filepath)
        all_results[ptype] = deps

    if args.json:
        print(json.dumps(all_results, indent=2))
    elif args.summary:
        for ptype, deps in all_results.items():
            total = sum(len(v) for v in deps.values())
            prod = len(deps.get("production", []))
            dev = len(deps.get("dev", []))
            peer = len(deps.get("peer", []))
            parts = [f"prod={prod}", f"dev={dev}"]
            if peer:
                parts.append(f"peer={peer}")
            print(f"{ptype}: {total} deps ({', '.join(parts)})")
    else:
        for ptype, deps in all_results.items():
            print(format_tree(ptype, deps, show_versions=not args.no_versions))


if __name__ == "__main__":
    main()
