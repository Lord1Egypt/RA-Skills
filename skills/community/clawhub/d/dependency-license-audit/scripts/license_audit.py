#!/usr/bin/env python3
"""Dependency License Auditor — scan project dependencies for license compatibility issues.

Supports: npm (package.json/package-lock.json), pip (requirements.txt/Pipfile/pyproject.toml),
Go (go.mod), Rust (Cargo.toml), Ruby (Gemfile), and generic SPDX detection.

Usage:
    python3 license_audit.py <project-dir> [--policy <policy>] [--format text|json|markdown] [--ci]

Policies:
    permissive  — Allow only permissive licenses (MIT, Apache-2.0, BSD, ISC, etc.)
    weak-copyleft — Also allow LGPL, MPL, EPL (weak copyleft)
    any-open    — Allow all OSI-approved licenses
    custom      — Read from .license-policy.json in project dir

Exit codes (with --ci):
    0 — No issues found
    1 — Warnings only (unknown licenses)
    2 — Policy violations found
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ─── License classification database ───

PERMISSIVE_LICENSES = {
    "MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0",
    "Unlicense", "CC0-1.0", "0BSD", "Zlib", "BSL-1.0",
    "MIT-0", "BlueOak-1.0.0", "CC-BY-4.0", "CC-BY-3.0",
    "PSF-2.0", "Python-2.0", "X11", "Artistic-2.0",
    "WTFPL", "Fair", "PostgreSQL", "Vim",
}

WEAK_COPYLEFT_LICENSES = {
    "LGPL-2.0-only", "LGPL-2.0-or-later", "LGPL-2.1-only", "LGPL-2.1-or-later",
    "LGPL-3.0-only", "LGPL-3.0-or-later",
    "MPL-2.0", "EPL-1.0", "EPL-2.0", "CDDL-1.0", "CDDL-1.1",
    "CPL-1.0", "OSL-3.0",
}

STRONG_COPYLEFT_LICENSES = {
    "GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later",
    "AGPL-3.0-only", "AGPL-3.0-or-later",
    "SSPL-1.0", "EUPL-1.1", "EUPL-1.2",
}

PROPRIETARY_INDICATORS = {
    "UNLICENSED", "PROPRIETARY", "SEE LICENSE IN", "Commercial",
}

# Common SPDX aliases / non-standard names → normalized
LICENSE_ALIASES = {
    "MIT License": "MIT",
    "The MIT License": "MIT",
    "ISC License": "ISC",
    "BSD": "BSD-3-Clause",
    "BSD License": "BSD-3-Clause",
    "2-Clause BSD": "BSD-2-Clause",
    "3-Clause BSD": "BSD-3-Clause",
    "New BSD": "BSD-3-Clause",
    "Simplified BSD": "BSD-2-Clause",
    "Apache 2.0": "Apache-2.0",
    "Apache License 2.0": "Apache-2.0",
    "Apache License, Version 2.0": "Apache-2.0",
    "Apache-2": "Apache-2.0",
    "GPLv2": "GPL-2.0-only",
    "GPLv3": "GPL-3.0-only",
    "GPL-2.0": "GPL-2.0-only",
    "GPL-3.0": "GPL-3.0-only",
    "GPL v2": "GPL-2.0-only",
    "GPL v3": "GPL-3.0-only",
    "LGPL-2.1": "LGPL-2.1-only",
    "LGPL-3.0": "LGPL-3.0-only",
    "LGPLv2.1": "LGPL-2.1-only",
    "LGPLv3": "LGPL-3.0-only",
    "AGPL-3.0": "AGPL-3.0-only",
    "AGPLv3": "AGPL-3.0-only",
    "MPL 2.0": "MPL-2.0",
    "MPL-2": "MPL-2.0",
    "Artistic-2": "Artistic-2.0",
    "CC0": "CC0-1.0",
    "CC-BY-4": "CC-BY-4.0",
    "Public Domain": "Unlicense",
    "WTFPL": "WTFPL",
    "Zlib": "Zlib",
    "PSF": "PSF-2.0",
    "Python": "Python-2.0",
    "EPL 1.0": "EPL-1.0",
    "EPL 2.0": "EPL-2.0",
    "Eclipse Public License 1.0": "EPL-1.0",
    "Eclipse Public License 2.0": "EPL-2.0",
    "CDDL 1.0": "CDDL-1.0",
    "CDDL": "CDDL-1.0",
    "Unlicense": "Unlicense",
    "UNLICENSED": "UNLICENSED",
}

ALL_KNOWN = PERMISSIVE_LICENSES | WEAK_COPYLEFT_LICENSES | STRONG_COPYLEFT_LICENSES


def normalize_license(raw: str) -> str:
    """Normalize a license string to SPDX identifier."""
    raw = raw.strip()
    # Strip parentheses from SPDX expressions like "(MIT OR GPL-3.0-or-later)"
    if raw.startswith("(") and raw.endswith(")"):
        raw = raw[1:-1].strip()
    if raw in ALL_KNOWN or raw in PROPRIETARY_INDICATORS:
        return raw
    if raw in LICENSE_ALIASES:
        return LICENSE_ALIASES[raw]
    # Case-insensitive lookup
    raw_lower = raw.lower()
    for alias, spdx in LICENSE_ALIASES.items():
        if alias.lower() == raw_lower:
            return spdx
    # Try to match SPDX expression (e.g., "MIT OR Apache-2.0")
    if " OR " in raw or " AND " in raw:
        return raw  # Keep as SPDX expression
    # Partial match
    for known in ALL_KNOWN:
        if known.lower() == raw_lower:
            return known
    return raw


def classify_license(license_id: str) -> str:
    """Classify a license: permissive, weak-copyleft, strong-copyleft, proprietary, unknown."""
    normalized = normalize_license(license_id)
    if normalized in PERMISSIVE_LICENSES:
        return "permissive"
    if normalized in WEAK_COPYLEFT_LICENSES:
        return "weak-copyleft"
    if normalized in STRONG_COPYLEFT_LICENSES:
        return "strong-copyleft"
    if normalized.upper() in PROPRIETARY_INDICATORS or any(p.lower() in normalized.lower() for p in PROPRIETARY_INDICATORS):
        return "proprietary"
    # Handle SPDX expressions
    if " OR " in normalized:
        parts = [p.strip() for p in normalized.split(" OR ")]
        classifications = [classify_license(p) for p in parts]
        # OR means choice — pick the most permissive
        for level in ["permissive", "weak-copyleft", "strong-copyleft"]:
            if level in classifications:
                return level
    if " AND " in normalized:
        parts = [p.strip() for p in normalized.split(" AND ")]
        classifications = [classify_license(p) for p in parts]
        # AND means all apply — pick the most restrictive
        for level in ["strong-copyleft", "weak-copyleft", "permissive"]:
            if level in classifications:
                return level
    return "unknown"


# ─── Ecosystem parsers ───

def parse_npm(project_dir: Path) -> list[dict]:
    """Parse npm dependencies from package.json and node_modules."""
    deps = []
    pkg_json = project_dir / "package.json"
    if not pkg_json.exists():
        return deps

    with open(pkg_json) as f:
        pkg = json.load(f)

    all_deps = {}
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        all_deps.update(pkg.get(key, {}))

    # Try to read licenses from node_modules
    node_modules = project_dir / "node_modules"
    for name, version_spec in all_deps.items():
        dep_info = {"name": name, "version": version_spec, "ecosystem": "npm", "license": "UNKNOWN"}

        # Handle scoped packages
        pkg_dir = node_modules / name
        dep_pkg = pkg_dir / "package.json"
        if dep_pkg.exists():
            try:
                with open(dep_pkg) as f:
                    dep_data = json.load(f)
                lic = dep_data.get("license", "")
                if isinstance(lic, dict):
                    lic = lic.get("type", "UNKNOWN")
                if isinstance(lic, list):
                    lic = " OR ".join(str(l.get("type", l) if isinstance(l, dict) else l) for l in lic)
                dep_info["license"] = str(lic) if lic else "UNKNOWN"
                dep_info["version"] = dep_data.get("version", version_spec)
            except (json.JSONDecodeError, KeyError):
                pass
        deps.append(dep_info)

    # Also scan package-lock.json for transitive deps
    lock_file = project_dir / "package-lock.json"
    if lock_file.exists():
        try:
            with open(lock_file) as f:
                lock = json.load(f)
            packages = lock.get("packages", {})
            for pkg_path, info in packages.items():
                if not pkg_path or pkg_path == "":
                    continue
                name = pkg_path.replace("node_modules/", "").split("node_modules/")[-1]
                if any(d["name"] == name for d in deps):
                    continue
                lic = info.get("license", "UNKNOWN")
                if isinstance(lic, dict):
                    lic = lic.get("type", "UNKNOWN")
                deps.append({
                    "name": name,
                    "version": info.get("version", "?"),
                    "ecosystem": "npm",
                    "license": str(lic) if lic else "UNKNOWN",
                    "transitive": True,
                })
        except (json.JSONDecodeError, KeyError):
            pass

    return deps


def parse_pip(project_dir: Path) -> list[dict]:
    """Parse Python dependencies from requirements.txt, Pipfile, or pyproject.toml."""
    deps = []

    # requirements.txt
    for req_file in project_dir.glob("requirements*.txt"):
        with open(req_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                # Parse "package==1.0.0" or "package>=1.0"
                match = re.match(r'^([a-zA-Z0-9_.-]+)\s*([><=!~]+\s*[\d.]+)?', line)
                if match:
                    name = match.group(1)
                    version = match.group(2) or "any"
                    deps.append({
                        "name": name, "version": version.strip(),
                        "ecosystem": "pip", "license": "UNKNOWN",
                    })

    # pyproject.toml (basic parsing)
    pyproject = project_dir / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text()
        # Simple regex for dependencies list
        dep_section = re.search(r'\[project\]\s*\n.*?dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if dep_section:
            for match in re.finditer(r'"([a-zA-Z0-9_.-]+)', dep_section.group(1)):
                name = match.group(1)
                if not any(d["name"] == name for d in deps):
                    deps.append({
                        "name": name, "version": "any",
                        "ecosystem": "pip", "license": "UNKNOWN",
                    })

    # Pipfile (basic parsing)
    pipfile = project_dir / "Pipfile"
    if pipfile.exists():
        content = pipfile.read_text()
        in_packages = False
        for line in content.split("\n"):
            if line.strip() in ("[packages]", "[dev-packages]"):
                in_packages = True
                continue
            if line.strip().startswith("["):
                in_packages = False
                continue
            if in_packages and "=" in line:
                name = line.split("=")[0].strip().strip('"')
                if name and not any(d["name"] == name for d in deps):
                    deps.append({
                        "name": name, "version": "any",
                        "ecosystem": "pip", "license": "UNKNOWN",
                    })

    # Try to read licenses from installed packages
    for dep in deps:
        if dep["license"] == "UNKNOWN":
            dep["license"] = _get_pip_license(dep["name"])

    return deps


def _get_pip_license(package_name: str) -> str:
    """Try to get license from pip metadata."""
    import importlib.metadata
    try:
        meta = importlib.metadata.metadata(package_name)
        lic = meta.get("License", "")
        if lic and lic != "UNKNOWN":
            return lic
        # Check classifiers
        classifiers = meta.get_all("Classifier") or []
        for c in classifiers:
            if c.startswith("License ::"):
                parts = c.split("::")
                return parts[-1].strip()
    except importlib.metadata.PackageNotFoundError:
        pass
    return "UNKNOWN"


def parse_go(project_dir: Path) -> list[dict]:
    """Parse Go dependencies from go.mod."""
    deps = []
    go_mod = project_dir / "go.mod"
    if not go_mod.exists():
        return deps

    content = go_mod.read_text()
    in_require = False
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("require ("):
            in_require = True
            continue
        if line == ")":
            in_require = False
            continue
        if in_require or line.startswith("require "):
            if line.startswith("require "):
                line = line[8:]
            parts = line.split()
            if len(parts) >= 2 and not parts[0].startswith("//"):
                deps.append({
                    "name": parts[0], "version": parts[1],
                    "ecosystem": "go", "license": "UNKNOWN",
                })

    return deps


def parse_cargo(project_dir: Path) -> list[dict]:
    """Parse Rust dependencies from Cargo.toml."""
    deps = []
    cargo = project_dir / "Cargo.toml"
    if not cargo.exists():
        return deps

    content = cargo.read_text()
    in_deps = False
    for line in content.split("\n"):
        line = line.strip()
        if line in ("[dependencies]", "[dev-dependencies]", "[build-dependencies]"):
            in_deps = True
            continue
        if line.startswith("[") and "dependencies" not in line:
            in_deps = False
            continue
        if in_deps and "=" in line:
            name = line.split("=")[0].strip()
            if name and not name.startswith("#"):
                version_match = re.search(r'"([^"]*)"', line)
                version = version_match.group(1) if version_match else "any"
                deps.append({
                    "name": name, "version": version,
                    "ecosystem": "cargo", "license": "UNKNOWN",
                })

    return deps


def parse_gemfile(project_dir: Path) -> list[dict]:
    """Parse Ruby dependencies from Gemfile."""
    deps = []
    gemfile = project_dir / "Gemfile"
    if not gemfile.exists():
        return deps

    content = gemfile.read_text()
    for match in re.finditer(r"gem\s+['\"]([^'\"]+)['\"]", content):
        deps.append({
            "name": match.group(1), "version": "any",
            "ecosystem": "gem", "license": "UNKNOWN",
        })

    return deps


# ─── Policy engine ───

POLICIES = {
    "permissive": {"allowed": {"permissive"}, "description": "Only permissive licenses (MIT, Apache-2.0, BSD, ISC, etc.)"},
    "weak-copyleft": {"allowed": {"permissive", "weak-copyleft"}, "description": "Permissive + weak copyleft (LGPL, MPL, EPL)"},
    "any-open": {"allowed": {"permissive", "weak-copyleft", "strong-copyleft"}, "description": "All OSI-approved open source licenses"},
}


def load_custom_policy(project_dir: Path) -> dict | None:
    """Load custom policy from .license-policy.json."""
    policy_file = project_dir / ".license-policy.json"
    if not policy_file.exists():
        return None
    with open(policy_file) as f:
        return json.load(f)


def check_policy(dep: dict, policy: dict, custom_policy: dict | None = None) -> dict | None:
    """Check a dependency against the policy. Returns violation dict or None."""
    license_id = normalize_license(dep["license"])
    classification = classify_license(license_id)

    # Custom policy overrides
    if custom_policy:
        allowed_licenses = set(custom_policy.get("allowed_licenses", []))
        blocked_licenses = set(custom_policy.get("blocked_licenses", []))
        allowed_classifications = set(custom_policy.get("allowed_classifications", []))
        exceptions = set(custom_policy.get("exceptions", []))

        if dep["name"] in exceptions:
            return None
        if license_id in blocked_licenses:
            return {
                "dep": dep, "license": license_id, "classification": classification,
                "severity": "error", "reason": f"License '{license_id}' is explicitly blocked by policy",
            }
        if allowed_licenses and license_id in allowed_licenses:
            return None
        if allowed_classifications and classification in allowed_classifications:
            return None
        if allowed_licenses or allowed_classifications:
            return {
                "dep": dep, "license": license_id, "classification": classification,
                "severity": "error", "reason": f"License '{license_id}' ({classification}) not in custom allowed list",
            }

    if classification == "unknown":
        return {
            "dep": dep, "license": license_id, "classification": classification,
            "severity": "warning", "reason": f"Unknown license '{license_id}' — manual review required",
        }
    if classification == "proprietary":
        return {
            "dep": dep, "license": license_id, "classification": classification,
            "severity": "error", "reason": f"Proprietary license detected",
        }
    if classification not in policy["allowed"]:
        return {
            "dep": dep, "license": license_id, "classification": classification,
            "severity": "error",
            "reason": f"{classification} license '{license_id}' violates '{list(policy['allowed'])}' policy",
        }

    return None


# ─── Recommendations ───

RECOMMENDATIONS = {
    "strong-copyleft": [
        "GPL/AGPL licenses require derivative works to be released under the same license",
        "If your project is proprietary, consider replacing this dependency with a permissively-licensed alternative",
        "If distributing, ensure your project's license is compatible (GPL-compatible)",
        "AGPL additionally requires providing source code to network users",
    ],
    "weak-copyleft": [
        "LGPL/MPL allow linking without license contamination if used as a library",
        "Modifications to the dependency itself must be shared under the same license",
        "Static linking may trigger stronger copyleft obligations — prefer dynamic linking",
    ],
    "proprietary": [
        "Verify you have a valid license agreement for commercial use",
        "Check if there's an open-source alternative available",
        "Ensure usage terms permit your intended use case",
    ],
    "unknown": [
        "Check the package's repository for a LICENSE file",
        "Contact the maintainer to clarify licensing terms",
        "Consider replacing with a clearly-licensed alternative",
        "Do not use in production until license is confirmed",
    ],
}


# ─── Output formatters ───

def format_text(deps: list, violations: list, policy_name: str, project_dir: str) -> str:
    lines = []
    lines.append(f"=== Dependency License Audit ===")
    lines.append(f"Project: {project_dir}")
    lines.append(f"Policy: {policy_name}")
    lines.append(f"Dependencies scanned: {len(deps)}")
    lines.append("")

    # Summary by ecosystem
    ecosystems = {}
    for d in deps:
        eco = d["ecosystem"]
        ecosystems[eco] = ecosystems.get(eco, 0) + 1
    for eco, count in sorted(ecosystems.items()):
        lines.append(f"  {eco}: {count} dependencies")
    lines.append("")

    # License distribution
    dist = {}
    for d in deps:
        cls = classify_license(normalize_license(d["license"]))
        dist[cls] = dist.get(cls, 0) + 1
    lines.append("License distribution:")
    for cls in ["permissive", "weak-copyleft", "strong-copyleft", "proprietary", "unknown"]:
        if cls in dist:
            lines.append(f"  {cls}: {dist[cls]}")
    lines.append("")

    errors = [v for v in violations if v["severity"] == "error"]
    warnings = [v for v in violations if v["severity"] == "warning"]

    if errors:
        lines.append(f"VIOLATIONS ({len(errors)}):")
        for v in errors:
            dep = v["dep"]
            lines.append(f"  ✗ {dep['ecosystem']}/{dep['name']}@{dep['version']}")
            lines.append(f"    License: {v['license']} ({v['classification']})")
            lines.append(f"    Reason: {v['reason']}")
            recs = RECOMMENDATIONS.get(v["classification"], [])
            if recs:
                lines.append(f"    Recommendations:")
                for r in recs:
                    lines.append(f"      → {r}")
            lines.append("")

    if warnings:
        lines.append(f"WARNINGS ({len(warnings)}):")
        for v in warnings:
            dep = v["dep"]
            lines.append(f"  ? {dep['ecosystem']}/{dep['name']}@{dep['version']}")
            lines.append(f"    License: {v['license']}")
            lines.append(f"    Reason: {v['reason']}")
            recs = RECOMMENDATIONS.get(v["classification"], [])
            if recs:
                for r in recs:
                    lines.append(f"      → {r}")
            lines.append("")

    if not errors and not warnings:
        lines.append("✓ All dependencies comply with the selected policy.")
    else:
        lines.append(f"Summary: {len(errors)} violation(s), {len(warnings)} warning(s)")

    return "\n".join(lines)


def format_json(deps: list, violations: list, policy_name: str, project_dir: str) -> str:
    result = {
        "project": project_dir,
        "policy": policy_name,
        "total_dependencies": len(deps),
        "violations": len([v for v in violations if v["severity"] == "error"]),
        "warnings": len([v for v in violations if v["severity"] == "warning"]),
        "dependencies": [],
        "issues": [],
    }
    for d in deps:
        normalized = normalize_license(d["license"])
        result["dependencies"].append({
            "name": d["name"],
            "version": d["version"],
            "ecosystem": d["ecosystem"],
            "license": normalized,
            "classification": classify_license(normalized),
            "transitive": d.get("transitive", False),
        })
    for v in violations:
        dep = v["dep"]
        result["issues"].append({
            "package": f"{dep['ecosystem']}/{dep['name']}",
            "version": dep["version"],
            "license": v["license"],
            "classification": v["classification"],
            "severity": v["severity"],
            "reason": v["reason"],
            "recommendations": RECOMMENDATIONS.get(v["classification"], []),
        })
    return json.dumps(result, indent=2)


def format_markdown(deps: list, violations: list, policy_name: str, project_dir: str) -> str:
    lines = []
    lines.append(f"# Dependency License Audit Report")
    lines.append(f"")
    lines.append(f"**Project:** `{project_dir}`")
    lines.append(f"**Policy:** {policy_name}")
    lines.append(f"**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Dependencies scanned:** {len(deps)}")
    lines.append("")

    errors = [v for v in violations if v["severity"] == "error"]
    warnings = [v for v in violations if v["severity"] == "warning"]

    if errors:
        lines.append(f"## ❌ Violations ({len(errors)})")
        lines.append("")
        lines.append("| Package | Version | License | Classification | Issue |")
        lines.append("|---------|---------|---------|----------------|-------|")
        for v in errors:
            dep = v["dep"]
            lines.append(f"| {dep['name']} | {dep['version']} | {v['license']} | {v['classification']} | {v['reason']} |")
        lines.append("")
        for v in errors:
            recs = RECOMMENDATIONS.get(v["classification"], [])
            if recs:
                dep = v["dep"]
                lines.append(f"### {dep['name']} — Recommendations")
                for r in recs:
                    lines.append(f"- {r}")
                lines.append("")

    if warnings:
        lines.append(f"## ⚠️ Warnings ({len(warnings)})")
        lines.append("")
        lines.append("| Package | Version | License | Issue |")
        lines.append("|---------|---------|---------|-------|")
        for v in warnings:
            dep = v["dep"]
            lines.append(f"| {dep['name']} | {dep['version']} | {v['license']} | {v['reason']} |")
        lines.append("")

    # Full dependency table
    lines.append(f"## All Dependencies ({len(deps)})")
    lines.append("")
    lines.append("| Package | Version | Ecosystem | License | Classification |")
    lines.append("|---------|---------|-----------|---------|----------------|")
    for d in sorted(deps, key=lambda x: (x["ecosystem"], x["name"])):
        normalized = normalize_license(d["license"])
        cls = classify_license(normalized)
        marker = ""
        if cls == "strong-copyleft":
            marker = " ⚠️"
        elif cls == "unknown":
            marker = " ❓"
        lines.append(f"| {d['name']} | {d['version']} | {d['ecosystem']} | {normalized} | {cls}{marker} |")
    lines.append("")

    if not errors and not warnings:
        lines.append("## ✅ Result: All Clear")
        lines.append("All dependencies comply with the selected policy.")
    else:
        lines.append(f"## Summary")
        lines.append(f"- **Violations:** {len(errors)}")
        lines.append(f"- **Warnings:** {len(warnings)}")
        lines.append(f"- **Clean:** {len(deps) - len(errors) - len(warnings)}")

    return "\n".join(lines)


# ─── Main ───

def scan_project(project_dir: Path) -> list[dict]:
    """Scan all supported ecosystems in the project directory."""
    all_deps = []
    all_deps.extend(parse_npm(project_dir))
    all_deps.extend(parse_pip(project_dir))
    all_deps.extend(parse_go(project_dir))
    all_deps.extend(parse_cargo(project_dir))
    all_deps.extend(parse_gemfile(project_dir))
    return all_deps


def main():
    parser = argparse.ArgumentParser(
        description="Scan project dependencies for license compatibility issues.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("project_dir", help="Project directory to scan")
    parser.add_argument("--policy", choices=["permissive", "weak-copyleft", "any-open", "custom"],
                        default="permissive", help="License policy (default: permissive)")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--ci", action="store_true",
                        help="CI mode: exit with non-zero code on violations")
    parser.add_argument("--include-transitive", action="store_true",
                        help="Include transitive dependencies (npm lock file)")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.is_dir():
        print(f"Error: '{project_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Scan
    deps = scan_project(project_dir)
    if not deps:
        print("No dependencies found. Supported: package.json, requirements.txt, Pipfile, pyproject.toml, go.mod, Cargo.toml, Gemfile")
        sys.exit(0)

    # Filter transitive if not requested
    if not args.include_transitive:
        deps = [d for d in deps if not d.get("transitive")]

    # Load policy
    custom_policy = None
    if args.policy == "custom":
        custom_policy = load_custom_policy(project_dir)
        if not custom_policy:
            print("Error: --policy custom requires .license-policy.json in project directory", file=sys.stderr)
            sys.exit(1)
        policy = {"allowed": set(custom_policy.get("allowed_classifications", []))}
    else:
        policy = POLICIES[args.policy]

    # Check
    violations = []
    for dep in deps:
        violation = check_policy(dep, policy, custom_policy)
        if violation:
            violations.append(violation)

    # Format output
    formatters = {"text": format_text, "json": format_json, "markdown": format_markdown}
    output = formatters[args.format](deps, violations, args.policy, str(project_dir))
    print(output)

    # CI exit code
    if args.ci:
        errors = [v for v in violations if v["severity"] == "error"]
        warnings = [v for v in violations if v["severity"] == "warning"]
        if errors:
            sys.exit(2)
        if warnings:
            sys.exit(1)
        sys.exit(0)


if __name__ == "__main__":
    main()
