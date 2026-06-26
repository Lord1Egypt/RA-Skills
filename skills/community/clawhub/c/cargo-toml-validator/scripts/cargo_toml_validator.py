#!/usr/bin/env python3
"""
Cargo.toml Validator
Validate Rust Cargo.toml manifests for dependency issues, missing metadata,
feature conflicts, workspace config, and crates.io publishing readiness.
Usage: python3 cargo_toml_validator.py <command> <file> [--strict] [--format text|json|summary]
Commands: validate, check, explain, suggest
"""

import sys
import os
import re
import json
import argparse
import tomllib
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_EDITIONS = {"2015", "2018", "2021", "2024"}
CURRENT_EDITIONS = {"2021", "2024"}
OUTDATED_EDITIONS = {"2015", "2018"}

# D6: Deprecated crate names -> suggested replacements
DEPRECATED_CRATES: dict[str, str] = {
    "failure": "anyhow or thiserror",
    "error-chain": "thiserror",
    "iron": "actix-web or axum",
    "rustc-serialize": "serde",
    "hyper 0.11": "hyper 1.x",
    "tokio 0.1": "tokio 1.x",
    "actix-web 3": "actix-web 4",
    "rocket 0.4": "rocket 0.5",
}

# Deprecated crate names that can be matched by name alone (no version check)
DEPRECATED_BY_NAME: dict[str, str] = {
    "failure": "anyhow or thiserror",
    "error-chain": "thiserror",
    "iron": "actix-web or axum",
    "rustc-serialize": "serde",
}

# Deprecated crate names that require version prefix check
DEPRECATED_BY_VERSION: dict[str, dict[str, str]] = {
    "hyper": {"0.11": "hyper 1.x"},
    "tokio": {"0.1": "tokio 1.x"},
    "actix-web": {"3": "actix-web 4"},
    "rocket": {"0.4": "rocket 0.5"},
}

# time crate: old versions (0.1, 0.2) -> suggest chrono or time 0.3+
# Handled separately since "time" is also a valid modern crate

DEPENDENCY_SECTIONS = [
    "dependencies",
    "dev-dependencies",
    "build-dependencies",
    "target",
]


# ---------------------------------------------------------------------------
# Finding class
# ---------------------------------------------------------------------------

class Finding:
    """A single validation finding."""

    SEVERITIES = ("error", "warning", "info")

    def __init__(self, rule_id: str, severity: str, message: str, detail: str = ""):
        assert severity in self.SEVERITIES, f"Invalid severity: {severity}"
        self.rule_id = rule_id
        self.severity = severity
        self.message = message
        self.detail = detail

    def to_dict(self) -> dict:
        d = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
        }
        if self.detail:
            d["detail"] = self.detail
        return d

    def __repr__(self):
        return f"Finding({self.rule_id}, {self.severity}, {self.message!r})"


# ---------------------------------------------------------------------------
# TOML loading
# ---------------------------------------------------------------------------

def load_config(path: str) -> tuple[dict | None, Finding | None]:
    """Load and parse a Cargo.toml file. Returns (data, error_finding)."""
    # S1: File not found or unreadable
    if not os.path.exists(path):
        return None, Finding("S1", "error", f"File not found: {path}")
    try:
        with open(path, "rb") as f:
            content = f.read()
    except OSError as e:
        return None, Finding("S1", "error", f"Cannot read file: {e}")

    # S2: Empty file
    if len(content.strip()) == 0:
        return None, Finding("S2", "error", "File is empty")

    # S3: Invalid TOML syntax
    try:
        data = tomllib.loads(content.decode("utf-8"))
    except tomllib.TOMLDecodeError as e:
        return None, Finding("S3", "error", f"Invalid TOML syntax: {e}")
    except UnicodeDecodeError as e:
        return None, Finding("S3", "error", f"File encoding error: {e}")

    return data, None


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------

def check_structure(data: dict) -> list[Finding]:
    """S4, S5: Check for [package] section and required fields."""
    findings: list[Finding] = []
    has_package = "package" in data
    has_workspace = "workspace" in data
    is_virtual_workspace = has_workspace and not has_package

    # S4: Missing [package] section
    if not has_package:
        if is_virtual_workspace:
            findings.append(Finding("S4", "warning",
                "No [package] section (virtual workspace)",
                "Virtual workspaces use [workspace] only. This is fine if intentional."))
        else:
            findings.append(Finding("S4", "error",
                "Missing [package] section",
                "Every binary or library crate needs a [package] section."))
        return findings

    # S5: Missing required fields in [package]
    pkg = data["package"]
    if "name" not in pkg:
        findings.append(Finding("S5", "error",
            "Missing required field: package.name"))
    if "version" not in pkg:
        # version can be inherited from workspace, check for that
        if not (isinstance(pkg.get("version"), dict) and pkg["version"].get("workspace")):
            findings.append(Finding("S5", "error",
                "Missing required field: package.version",
                "Set version directly or use version.workspace = true."))
    if "edition" not in pkg:
        findings.append(Finding("S5", "warning",
            "Missing recommended field: package.edition",
            "Without edition, Rust defaults to 2015. Almost certainly wrong for new projects."))

    return findings


def check_package_metadata(data: dict) -> list[Finding]:
    """M1-M4: Check package metadata quality."""
    findings: list[Finding] = []
    pkg = data.get("package", {})

    if not pkg:
        return findings

    # M1: Missing edition field
    edition = pkg.get("edition")
    if edition is None:
        findings.append(Finding("M1", "warning",
            "Missing edition field — defaults to 2015",
            "Add edition = \"2021\" or edition = \"2024\" to [package]."))

    # M2: Outdated edition
    if edition is not None:
        edition_str = str(edition)
        if edition_str in OUTDATED_EDITIONS:
            findings.append(Finding("M2", "info",
                f"Outdated edition '{edition_str}' — consider upgrading to 2021 or 2024",
                "Run 'cargo fix --edition' to migrate."))
        elif edition_str not in VALID_EDITIONS:
            findings.append(Finding("M2", "warning",
                f"Unknown edition '{edition_str}' — valid editions: {', '.join(sorted(VALID_EDITIONS))}"))

    # M3: Missing license or license-file
    if "license" not in pkg and "license-file" not in pkg:
        findings.append(Finding("M3", "warning",
            "Missing license or license-file for crates.io publishing",
            "Add license = \"MIT\" or license-file = \"LICENSE\" to [package]."))

    # M4: Missing description
    if "description" not in pkg:
        findings.append(Finding("M4", "warning",
            "Missing description for crates.io publishing",
            "Add description = \"...\" to [package]. Required for crates.io."))

    return findings


def _extract_all_dependencies(data: dict) -> dict[str, dict[str, Any]]:
    """Extract all dependency sections. Returns {section_name: {dep_name: dep_spec}}."""
    result = {}

    for section in ["dependencies", "dev-dependencies", "build-dependencies"]:
        if section in data:
            result[section] = data[section]

    # Also extract target-specific dependencies
    targets = data.get("target", {})
    if isinstance(targets, dict):
        for target_name, target_data in targets.items():
            if isinstance(target_data, dict):
                for section in ["dependencies", "dev-dependencies", "build-dependencies"]:
                    if section in target_data:
                        key = f"target.{target_name}.{section}"
                        result[key] = target_data[section]

    return result


def _parse_version_from_dep(dep_spec: Any) -> str | None:
    """Extract version string from a dependency specification."""
    if isinstance(dep_spec, str):
        return dep_spec
    if isinstance(dep_spec, dict):
        return dep_spec.get("version")
    return None


def _is_git_dep(dep_spec: Any) -> bool:
    """Check if dependency uses git source."""
    if isinstance(dep_spec, dict):
        return "git" in dep_spec
    return False


def _is_path_dep(dep_spec: Any) -> bool:
    """Check if dependency uses path source."""
    if isinstance(dep_spec, dict):
        return "path" in dep_spec
    return False


def _git_is_pinned(dep_spec: dict) -> bool:
    """Check if a git dependency is pinned to rev, tag, or branch."""
    return any(k in dep_spec for k in ("rev", "tag", "branch"))


def check_dependencies(data: dict) -> list[Finding]:
    """D1-D6: Check dependency declarations."""
    findings: list[Finding] = []
    all_deps = _extract_all_dependencies(data)

    for section_name, deps in all_deps.items():
        if not isinstance(deps, dict):
            continue

        for dep_name, dep_spec in deps.items():
            version = _parse_version_from_dep(dep_spec)

            # D1: Wildcard version
            if version is not None and version.strip() == "*":
                findings.append(Finding("D1", "error",
                    f"Wildcard version '*' for '{dep_name}' in [{section_name}]",
                    "Wildcard dependencies are highly discouraged. Pin to a version range."))

            # D2: Unpinned dependency (empty version in table form)
            if isinstance(dep_spec, dict) and "version" not in dep_spec:
                if not _is_git_dep(dep_spec) and not _is_path_dep(dep_spec):
                    # Check for workspace inheritance
                    if not dep_spec.get("workspace"):
                        findings.append(Finding("D2", "warning",
                            f"Dependency '{dep_name}' in [{section_name}] has no version specifier",
                            "Add a version field or use workspace = true."))

            # D3: Git dependency without pin
            if _is_git_dep(dep_spec) and isinstance(dep_spec, dict):
                if not _git_is_pinned(dep_spec):
                    git_url = dep_spec.get("git", "")
                    findings.append(Finding("D3", "warning",
                        f"Git dependency '{dep_name}' in [{section_name}] is not pinned",
                        f"Pin to a rev, tag, or branch for reproducibility. URL: {git_url}"))

            # D4: Path dependency
            if _is_path_dep(dep_spec) and isinstance(dep_spec, dict):
                path_val = dep_spec.get("path", "")
                findings.append(Finding("D4", "info",
                    f"Path dependency '{dep_name}' in [{section_name}] — blocks crates.io publish",
                    f"Path: {path_val}. Fine for local dev, but won't work on crates.io."))

            # D6: Deprecated crate names (by name alone)
            if dep_name in DEPRECATED_BY_NAME:
                replacement = DEPRECATED_BY_NAME[dep_name]
                findings.append(Finding("D6", "info",
                    f"Deprecated crate '{dep_name}' in [{section_name}] — consider '{replacement}'",
                    f"'{dep_name}' is unmaintained. Migrate to {replacement}."))

            # D6: Deprecated crate names (by version prefix)
            if dep_name in DEPRECATED_BY_VERSION and version is not None:
                for prefix, replacement in DEPRECATED_BY_VERSION[dep_name].items():
                    # Check if version starts with the deprecated major version
                    clean_ver = version.lstrip("^~>=<! ")
                    if clean_ver.startswith(prefix):
                        findings.append(Finding("D6", "info",
                            f"Outdated version of '{dep_name}' ({version}) in [{section_name}] — consider '{replacement}'",
                            f"Upgrade to {replacement} for latest features and fixes."))
                        break

            # D6: Special handling for 'time' crate
            if dep_name == "time" and version is not None:
                clean_ver = version.lstrip("^~>=<! ")
                if clean_ver.startswith("0.1") or clean_ver.startswith("0.2"):
                    findings.append(Finding("D6", "info",
                        f"Outdated 'time' crate ({version}) in [{section_name}] — consider chrono or time 0.3+",
                        "time 0.1/0.2 are unmaintained. Use chrono or time 0.3+."))

    # D5: Duplicate dependency in [dependencies] and [dev-dependencies] with different versions
    main_deps = all_deps.get("dependencies", {})
    dev_deps = all_deps.get("dev-dependencies", {})
    if main_deps and dev_deps:
        overlap = set(main_deps.keys()) & set(dev_deps.keys())
        for dep_name in sorted(overlap):
            main_ver = _parse_version_from_dep(main_deps[dep_name])
            dev_ver = _parse_version_from_dep(dev_deps[dep_name])
            if main_ver != dev_ver:
                findings.append(Finding("D5", "warning",
                    f"'{dep_name}' in both [dependencies] ({main_ver}) and [dev-dependencies] ({dev_ver}) with different versions",
                    "This can cause confusing build behavior. Align versions or use features."))

    return findings


def check_features(data: dict) -> list[Finding]:
    """F1-F3: Check feature declarations."""
    findings: list[Finding] = []
    features = data.get("features", {})

    if not features:
        return findings

    # Build set of known dependency names (for F1 check)
    known_deps: set[str] = set()
    all_deps = _extract_all_dependencies(data)
    for section_deps in all_deps.values():
        if isinstance(section_deps, dict):
            known_deps.update(section_deps.keys())

    # Also add optional dependencies (they can be enabled as features)
    main_deps = data.get("dependencies", {})
    optional_deps: set[str] = set()
    if isinstance(main_deps, dict):
        for dep_name, dep_spec in main_deps.items():
            if isinstance(dep_spec, dict) and dep_spec.get("optional"):
                optional_deps.add(dep_name)

    # All feature names are also valid as feature references
    feature_names = set(features.keys())

    for feat_name, feat_values in features.items():
        if not isinstance(feat_values, list):
            continue

        # F2: Empty feature
        if len(feat_values) == 0:
            findings.append(Finding("F2", "warning",
                f"Feature '{feat_name}' is empty (no dependencies or sub-features)",
                "Empty features serve no purpose. Add entries or remove."))
            continue

        # F1: Feature enables non-existent dependency
        for entry in feat_values:
            if not isinstance(entry, str):
                continue

            # Features can reference:
            # - "dep:crate_name" (explicit dep activation)
            # - "crate_name/feature" (enable feature on a dep)
            # - "another_feature" (enable another feature)
            if entry.startswith("dep:"):
                dep_ref = entry[4:]
                if dep_ref not in known_deps:
                    findings.append(Finding("F1", "error",
                        f"Feature '{feat_name}' enables non-existent dependency 'dep:{dep_ref}'",
                        f"No dependency named '{dep_ref}' found in any dependency section."))
            elif "/" in entry:
                dep_ref = entry.split("/")[0]
                if dep_ref not in known_deps and dep_ref not in feature_names:
                    findings.append(Finding("F1", "error",
                        f"Feature '{feat_name}' references unknown dependency '{dep_ref}' in '{entry}'",
                        f"No dependency or feature named '{dep_ref}' found."))
            else:
                # Could be a feature name or an optional dep name
                if entry not in feature_names and entry not in optional_deps and entry not in known_deps:
                    findings.append(Finding("F1", "error",
                        f"Feature '{feat_name}' references unknown item '{entry}'",
                        f"'{entry}' is not a known feature, dependency, or optional dependency."))

    # F3: Circular feature dependencies
    # Build adjacency graph and detect cycles
    graph: dict[str, list[str]] = {}
    for feat_name, feat_values in features.items():
        if not isinstance(feat_values, list):
            continue
        deps_list: list[str] = []
        for entry in feat_values:
            if isinstance(entry, str) and not entry.startswith("dep:") and "/" not in entry:
                # This could be a reference to another feature
                if entry in feature_names:
                    deps_list.append(entry)
        graph[feat_name] = deps_list

    # DFS cycle detection
    visited: set[str] = set()
    rec_stack: set[str] = set()
    cycles_found: set[str] = set()

    def _dfs(node: str, path: list[str]) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if _dfs(neighbor, path + [neighbor]):
                    return True
            elif neighbor in rec_stack:
                cycle_key = "->".join(path + [neighbor])
                if cycle_key not in cycles_found:
                    cycles_found.add(cycle_key)
                    findings.append(Finding("F3", "error",
                        f"Circular feature dependency detected: {' -> '.join(path + [neighbor])}",
                        "Circular features cause compilation errors."))
                return True
        rec_stack.discard(node)
        return False

    for feat in graph:
        if feat not in visited:
            _dfs(feat, [feat])

    return findings


def check_workspace(data: dict) -> list[Finding]:
    """W1-W3: Check workspace configuration."""
    findings: list[Finding] = []
    workspace = data.get("workspace")
    has_package = "package" in data

    if workspace is None:
        return findings

    if not isinstance(workspace, dict):
        return findings

    members = workspace.get("members", [])

    # W1: Workspace with no members
    if not members:
        findings.append(Finding("W1", "warning",
            "[workspace] has no members defined",
            "Add members = [\"crate-a\", \"crate-b\"] to list workspace crates."))

    # W2: Both [package] and [workspace] without workspace.members
    if has_package and not members:
        findings.append(Finding("W2", "info",
            "Both [package] and [workspace] present but no workspace.members",
            "This is a single-crate workspace. Add members if you intend a multi-crate workspace."))

    # W3: Workspace dependencies hint
    ws_deps = workspace.get("dependencies")
    if ws_deps and isinstance(ws_deps, dict):
        dep_names = ", ".join(sorted(list(ws_deps.keys())[:5]))
        total = len(ws_deps)
        suffix = f" (and {total - 5} more)" if total > 5 else ""
        findings.append(Finding("W3", "info",
            f"[workspace.dependencies] defines {total} shared dependencies: {dep_names}{suffix}",
            "Member crates must use dep_name.workspace = true to inherit these. "
            "Cannot verify from a single Cargo.toml alone."))

    return findings


def check_best_practices(data: dict) -> list[Finding]:
    """B1-B4: Check best practices."""
    findings: list[Finding] = []
    pkg = data.get("package", {})

    if not pkg:
        return findings

    # B1: Missing documentation link
    metadata = pkg.get("metadata", {})
    has_docs = "documentation" in pkg
    has_docs_meta = isinstance(metadata, dict) and "docs" in metadata
    if not has_docs and not has_docs_meta:
        findings.append(Finding("B1", "info",
            "Missing documentation link for published crates",
            "Add documentation = \"https://docs.rs/your-crate\" to [package]."))

    # B2: build.rs without [build-dependencies]
    build_script = pkg.get("build")
    has_build_deps = "build-dependencies" in data
    if build_script is not None and not has_build_deps:
        findings.append(Finding("B2", "info",
            f"Build script declared (build = \"{build_script}\") but no [build-dependencies] section",
            "If your build script uses external crates, declare them in [build-dependencies]."))

    # B3: Large number of dependencies
    main_deps = data.get("dependencies", {})
    dep_count = len(main_deps) if isinstance(main_deps, dict) else 0
    if dep_count > 30:
        findings.append(Finding("B3", "info",
            f"Large number of dependencies ({dep_count}) — potential bloat",
            "Consider auditing dependencies for unused or redundant crates. "
            "Use 'cargo udeps' to find unused dependencies."))

    # B4: Missing repository/homepage URL
    has_repo = "repository" in pkg
    has_homepage = "homepage" in pkg
    if not has_repo and not has_homepage:
        findings.append(Finding("B4", "info",
            "Missing repository and homepage URL",
            "Add repository = \"https://github.com/...\" to [package] for crates.io visibility."))

    return findings


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def validate_all(data: dict) -> list[Finding]:
    """Run all checks and return combined findings."""
    findings: list[Finding] = []
    findings.extend(check_structure(data))
    findings.extend(check_package_metadata(data))
    findings.extend(check_dependencies(data))
    findings.extend(check_features(data))
    findings.extend(check_workspace(data))
    findings.extend(check_best_practices(data))
    return findings


# ---------------------------------------------------------------------------
# Rule explanations (for 'explain' command)
# ---------------------------------------------------------------------------

RULE_EXPLANATIONS: dict[str, dict[str, str]] = {
    "S1": {
        "name": "File Not Found",
        "category": "Structure",
        "severity": "error",
        "description": "The Cargo.toml file does not exist or cannot be read.",
        "fix": "Ensure the file path is correct and the file has read permissions.",
    },
    "S2": {
        "name": "Empty File",
        "category": "Structure",
        "severity": "error",
        "description": "The Cargo.toml file is empty (zero bytes or only whitespace).",
        "fix": "Add at minimum a [package] section with name, version, and edition.",
    },
    "S3": {
        "name": "Invalid TOML",
        "category": "Structure",
        "severity": "error",
        "description": "The file contains invalid TOML syntax that cannot be parsed.",
        "fix": "Fix the TOML syntax error reported in the message. Use a TOML linter.",
    },
    "S4": {
        "name": "Missing [package]",
        "category": "Structure",
        "severity": "error/warning",
        "description": "No [package] section found. Required for binary/library crates, optional for virtual workspaces.",
        "fix": "Add [package] with name, version, and edition. Virtual workspaces use [workspace] only.",
    },
    "S5": {
        "name": "Missing Required Fields",
        "category": "Structure",
        "severity": "error/warning",
        "description": "Missing name, version (error), or edition (warning) in [package].",
        "fix": "Add the missing fields. Example: name = \"my-crate\", version = \"0.1.0\", edition = \"2021\".",
    },
    "M1": {
        "name": "Missing Edition",
        "category": "Package Metadata",
        "severity": "warning",
        "description": "No edition field — Rust defaults to 2015, which is almost certainly wrong for new projects.",
        "fix": "Add edition = \"2021\" or edition = \"2024\" to [package].",
    },
    "M2": {
        "name": "Outdated Edition",
        "category": "Package Metadata",
        "severity": "info",
        "description": "Using an old Rust edition (2015 or 2018) when 2021/2024 are available.",
        "fix": "Run 'cargo fix --edition' to migrate, then update edition in Cargo.toml.",
    },
    "M3": {
        "name": "Missing License",
        "category": "Package Metadata",
        "severity": "warning",
        "description": "No license or license-file field. Required for crates.io publishing.",
        "fix": "Add license = \"MIT\" (or your license) or license-file = \"LICENSE\".",
    },
    "M4": {
        "name": "Missing Description",
        "category": "Package Metadata",
        "severity": "warning",
        "description": "No description field. Required for crates.io publishing.",
        "fix": "Add description = \"A short description of your crate.\" to [package].",
    },
    "D1": {
        "name": "Wildcard Version",
        "category": "Dependencies",
        "severity": "error",
        "description": "Using '*' as a version — allows any version, including breaking changes.",
        "fix": "Pin to a version range: serde = \"1\" or serde = \"^1.0\".",
    },
    "D2": {
        "name": "Unpinned Dependency",
        "category": "Dependencies",
        "severity": "warning",
        "description": "Dependency declared as a table but has no version, git, path, or workspace source.",
        "fix": "Add version = \"x.y\" or use workspace = true to inherit from workspace.",
    },
    "D3": {
        "name": "Unpinned Git Dependency",
        "category": "Dependencies",
        "severity": "warning",
        "description": "Git dependency without rev, tag, or branch — tracks default branch HEAD.",
        "fix": "Add rev = \"abc123\", tag = \"v1.0\", or branch = \"main\" for reproducibility.",
    },
    "D4": {
        "name": "Path Dependency",
        "category": "Dependencies",
        "severity": "info",
        "description": "Using a path dependency. Works locally but blocks crates.io publishing.",
        "fix": "For publishing, add a version field alongside path for fallback.",
    },
    "D5": {
        "name": "Duplicate Dependency Versions",
        "category": "Dependencies",
        "severity": "warning",
        "description": "Same crate in [dependencies] and [dev-dependencies] with different version specs.",
        "fix": "Align the version specs or use features to differentiate test vs runtime needs.",
    },
    "D6": {
        "name": "Deprecated Crate",
        "category": "Dependencies",
        "severity": "info",
        "description": "Using a crate that is deprecated or has a well-known successor.",
        "fix": "Migrate to the suggested replacement crate.",
    },
    "F1": {
        "name": "Non-existent Feature Dependency",
        "category": "Features",
        "severity": "error",
        "description": "A feature references a dependency or feature that doesn't exist.",
        "fix": "Add the missing dependency or correct the feature reference.",
    },
    "F2": {
        "name": "Empty Feature",
        "category": "Features",
        "severity": "warning",
        "description": "A feature is defined with no entries — it enables nothing.",
        "fix": "Add dependency or feature entries, or remove the empty feature.",
    },
    "F3": {
        "name": "Circular Feature",
        "category": "Features",
        "severity": "error",
        "description": "Features reference each other in a cycle, which causes compilation errors.",
        "fix": "Break the cycle by restructuring feature dependencies.",
    },
    "W1": {
        "name": "Empty Workspace",
        "category": "Workspace",
        "severity": "warning",
        "description": "[workspace] section exists but has no members listed.",
        "fix": "Add members = [\"crate-a\", \"crate-b\"] to [workspace].",
    },
    "W2": {
        "name": "Ambiguous Workspace",
        "category": "Workspace",
        "severity": "info",
        "description": "Both [package] and [workspace] present without workspace.members.",
        "fix": "Add members if multi-crate workspace, or remove [workspace] if single crate.",
    },
    "W3": {
        "name": "Workspace Dependencies Hint",
        "category": "Workspace",
        "severity": "info",
        "description": "[workspace.dependencies] found — member crates must use workspace = true to inherit.",
        "fix": "In member Cargo.toml files, use: dep_name = { workspace = true }.",
    },
    "B1": {
        "name": "Missing Docs Link",
        "category": "Best Practices",
        "severity": "info",
        "description": "No documentation URL for published crates.",
        "fix": "Add documentation = \"https://docs.rs/your-crate\" to [package].",
    },
    "B2": {
        "name": "Build Script Without Build-Dependencies",
        "category": "Best Practices",
        "severity": "info",
        "description": "A build script is declared but no [build-dependencies] section exists.",
        "fix": "If the build script uses external crates, declare them in [build-dependencies].",
    },
    "B3": {
        "name": "Dependency Bloat",
        "category": "Best Practices",
        "severity": "info",
        "description": "More than 30 dependencies — may indicate bloat.",
        "fix": "Audit with 'cargo udeps' for unused deps. Consider feature flags for optional deps.",
    },
    "B4": {
        "name": "Missing Repository URL",
        "category": "Best Practices",
        "severity": "info",
        "description": "No repository or homepage URL in [package].",
        "fix": "Add repository = \"https://github.com/user/repo\" to [package].",
    },
}


# ---------------------------------------------------------------------------
# Suggestion engine (for 'suggest' command)
# ---------------------------------------------------------------------------

def generate_suggestions(data: dict, findings: list[Finding]) -> list[dict]:
    """Generate actionable fix suggestions from findings."""
    suggestions: list[dict] = []

    for f in findings:
        rule = RULE_EXPLANATIONS.get(f.rule_id)
        if not rule:
            continue

        suggestion = {
            "rule_id": f.rule_id,
            "severity": f.severity,
            "problem": f.message,
            "fix": rule["fix"],
        }

        # Add concrete TOML snippets for common fixes
        pkg = data.get("package", {})
        pkg_name = pkg.get("name", "my-crate")

        if f.rule_id == "S5" and "name" in f.message:
            suggestion["snippet"] = '[package]\nname = "my-crate"'
        elif f.rule_id == "S5" and "version" in f.message:
            suggestion["snippet"] = 'version = "0.1.0"'
        elif f.rule_id == "S5" and "edition" in f.message:
            suggestion["snippet"] = 'edition = "2021"'
        elif f.rule_id == "M1":
            suggestion["snippet"] = 'edition = "2021"'
        elif f.rule_id == "M3":
            suggestion["snippet"] = 'license = "MIT"'
        elif f.rule_id == "M4":
            suggestion["snippet"] = f'description = "A Rust crate for ..."'
        elif f.rule_id == "B4":
            suggestion["snippet"] = f'repository = "https://github.com/user/{pkg_name}"'
        elif f.rule_id == "D1":
            # Extract dep name from message (second quoted string — first is '*')
            dep_matches = re.findall(r"'([^']+)'", f.message)
            if len(dep_matches) >= 2:
                dep = dep_matches[1]
                suggestion["snippet"] = f'{dep} = "1"  # pin to a version'

        suggestions.append(suggestion)

    return suggestions


# ---------------------------------------------------------------------------
# Summary helper
# ---------------------------------------------------------------------------

def _summary_counts(findings: list[Finding]) -> dict:
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    infos = sum(1 for f in findings if f.severity == "info")
    return {"errors": errors, "warnings": warnings, "infos": infos, "total": len(findings)}


def _summary_text(findings: list[Finding]) -> str:
    c = _summary_counts(findings)
    parts = []
    if c["errors"]:
        parts.append(f"{c['errors']} error(s)")
    if c["warnings"]:
        parts.append(f"{c['warnings']} warning(s)")
    if c["infos"]:
        parts.append(f"{c['infos']} info")
    return ", ".join(parts) if parts else "No issues found"


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_validate(data: dict, path: str) -> dict:
    """Full validation with summary."""
    findings = validate_all(data)
    errors = [f for f in findings if f.severity == "error"]
    return {
        "command": "validate",
        "file": path,
        "valid": len(errors) == 0,
        "findings": [f.to_dict() for f in findings],
        "counts": _summary_counts(findings),
        "summary": _summary_text(findings),
    }


def cmd_check(data: dict, path: str) -> dict:
    """Quick check — errors and warnings only."""
    findings = validate_all(data)
    filtered = [f for f in findings if f.severity in ("error", "warning")]
    return {
        "command": "check",
        "file": path,
        "passed": all(f.severity != "error" for f in findings),
        "findings": [f.to_dict() for f in filtered],
        "counts": _summary_counts(filtered),
        "summary": _summary_text(filtered),
    }


def cmd_explain(data: dict | None, path: str) -> dict:
    """Explain all rules with their categories and severity."""
    rules = []
    for rule_id in sorted(RULE_EXPLANATIONS.keys()):
        info = RULE_EXPLANATIONS[rule_id]
        rules.append({
            "rule_id": rule_id,
            "name": info["name"],
            "category": info["category"],
            "severity": info["severity"],
            "description": info["description"],
            "fix": info["fix"],
        })
    return {
        "command": "explain",
        "file": path,
        "rules": rules,
        "total_rules": len(rules),
    }


def cmd_suggest(data: dict, path: str) -> dict:
    """Run validation and generate fix suggestions."""
    findings = validate_all(data)
    suggestions = generate_suggestions(data, findings)
    return {
        "command": "suggest",
        "file": path,
        "suggestions": suggestions,
        "total": len(suggestions),
        "summary": _summary_text(findings),
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    title = f"Cargo.toml {cmd} — {path}"
    lines.append(title)
    lines.append("=" * len(title))

    if cmd == "explain":
        for rule in result.get("rules", []):
            lines.append("")
            lines.append(f"  {rule['rule_id']}: {rule['name']} [{rule['category']}] ({rule['severity']})")
            lines.append(f"    {rule['description']}")
            lines.append(f"    Fix: {rule['fix']}")
        lines.append("")
        lines.append(f"Total rules: {result.get('total_rules', 0)}")
        return "\n".join(lines)

    if cmd == "suggest":
        suggestions = result.get("suggestions", [])
        if not suggestions:
            lines.append("[OK] No suggestions — Cargo.toml looks good")
        else:
            for s in suggestions:
                sev = s["severity"].upper().ljust(7)
                lines.append(f"[{sev}] {s['rule_id']}: {s['problem']}")
                lines.append(f"         Fix: {s['fix']}")
                if "snippet" in s:
                    lines.append(f"         Add: {s['snippet']}")
                lines.append("")
        lines.append(f"Summary: {result.get('summary', '')}")
        return "\n".join(lines)

    # validate / check
    findings = result.get("findings", [])
    if not findings:
        lines.append("[OK] No issues found")
    else:
        for f in findings:
            sev = f["severity"].upper().ljust(7)
            lines.append(f"[{sev}] {f['rule_id']}: {f['message']}")
            if f.get("detail"):
                lines.append(f"         {f['detail']}")

    if cmd == "validate":
        valid_str = "VALID" if result.get("valid") else "INVALID"
        lines.append("")
        lines.append(f"Result: {valid_str}")

    if cmd == "check":
        passed_str = "PASSED" if result.get("passed") else "FAILED"
        lines.append("")
        lines.append(f"Result: {passed_str}")

    summary = result.get("summary")
    if summary:
        lines.append(f"Summary: {summary}")

    return "\n".join(lines)


def format_json(result: dict) -> str:
    return json.dumps(result, indent=2)


def format_summary(result: dict) -> str:
    cmd = result.get("command", "")
    path = result.get("file", "")
    lines = []
    lines.append(f"Cargo.toml {cmd}: {path}")

    if cmd == "explain":
        lines.append(f"Rules: {result.get('total_rules', 0)}")
        categories: dict[str, int] = {}
        for rule in result.get("rules", []):
            cat = rule["category"]
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items()):
            lines.append(f"  {cat}: {count} rules")
        return "\n".join(lines)

    counts = result.get("counts", {})
    lines.append(f"Errors: {counts.get('errors', 0)}")
    lines.append(f"Warnings: {counts.get('warnings', 0)}")
    lines.append(f"Info: {counts.get('infos', 0)}")

    if "valid" in result:
        lines.append(f"Valid: {'yes' if result['valid'] else 'no'}")
    if "passed" in result:
        lines.append(f"Passed: {'yes' if result['passed'] else 'no'}")

    if cmd == "suggest":
        lines.append(f"Suggestions: {result.get('total', 0)}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate Rust Cargo.toml manifests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Commands:
  validate   Full validation with all rules
  check      Quick check (errors and warnings only)
  explain    Show all rules with descriptions
  suggest    Run validation and propose fixes

Examples:
  python3 cargo_toml_validator.py validate Cargo.toml
  python3 cargo_toml_validator.py validate Cargo.toml --strict
  python3 cargo_toml_validator.py check Cargo.toml --format json
  python3 cargo_toml_validator.py explain Cargo.toml
  python3 cargo_toml_validator.py suggest Cargo.toml --format summary
"""
    )
    parser.add_argument("command", choices=["validate", "check", "explain", "suggest"],
                        help="Command to run")
    parser.add_argument("file", help="Path to Cargo.toml")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (CI mode)")
    parser.add_argument("--format", choices=["text", "json", "summary"], default="text",
                        help="Output format (default: text)")

    args = parser.parse_args()

    # For 'explain', we don't need a valid file (but accept the arg for consistency)
    if args.command == "explain":
        result = cmd_explain(None, args.file)
    else:
        # Load and parse file
        data, parse_error = load_config(args.file)
        if parse_error:
            result = {
                "command": args.command,
                "file": args.file,
                "findings": [parse_error.to_dict()],
                "counts": {"errors": 1, "warnings": 0, "infos": 0, "total": 1},
                "summary": "1 error(s)",
            }
            if args.command == "validate":
                result["valid"] = False
            elif args.command == "check":
                result["passed"] = False
            elif args.command == "suggest":
                result["suggestions"] = []
                result["total"] = 0

            formatter = {"text": format_text, "json": format_json, "summary": format_summary}
            print(formatter[args.format](result))
            sys.exit(2)

        # Run command
        if args.command == "validate":
            result = cmd_validate(data, args.file)
        elif args.command == "check":
            result = cmd_check(data, args.file)
        elif args.command == "suggest":
            result = cmd_suggest(data, args.file)

    # Format output
    formatter = {"text": format_text, "json": format_json, "summary": format_summary}
    print(formatter[args.format](result))

    # Exit code
    if args.command == "explain":
        sys.exit(0)

    findings = result.get("findings", [])
    has_errors = any(f["severity"] == "error" for f in findings)
    has_warnings = any(f["severity"] == "warning" for f in findings)

    if has_errors:
        sys.exit(1)
    if args.strict and has_warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
