#!/usr/bin/env python3
"""devcontainer.json validator."""

import argparse
import json
import os
import re
import sys

SEVERITIES = {"error": 3, "warning": 2, "info": 1}

KNOWN_TOP_LEVEL_KEYS = {
    "name", "image", "dockerFile", "dockerComposeFile", "context", "build",
    "features", "customizations", "forwardPorts", "portsAttributes",
    "postCreateCommand", "postStartCommand", "postAttachCommand",
    "onCreateCommand", "updateContentCommand", "waitFor",
    "remoteUser", "containerUser", "remoteEnv", "containerEnv",
    "mounts", "runArgs", "overrideCommand", "shutdownAction",
    "init", "privileged", "capAdd", "securityOpt",
    "workspaceFolder", "workspaceMount",
}

LIFECYCLE_COMMANDS = [
    "postCreateCommand", "postStartCommand", "postAttachCommand",
    "onCreateCommand", "updateContentCommand",
]

DANGEROUS_CAPS = {"SYS_ADMIN", "NET_ADMIN", "SYS_PTRACE", "SYS_RAWIO", "NET_RAW"}

SHELL_INJECTION_PATTERNS = [
    (r'\brm\s+-rf\s+/', "rm -rf / detected"),
    (r'curl\s+[^\|]*\|\s*(ba)?sh', "curl piped to shell"),
    (r'wget\s+[^\|]*\|\s*(ba)?sh', "wget piped to shell"),
    (r'chmod\s+777\b', "chmod 777 detected"),
    (r'\beval\s+', "eval usage detected"),
    (r'>\s*/dev/sd[a-z]', "writing to raw block device"),
    (r'mkfs\b', "mkfs (format disk) detected"),
    (r':(){ :\|:& };:', "fork bomb detected"),
]

EXTENSION_ID_RE = re.compile(r'^[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$')
OCI_REF_RE = re.compile(
    r'^(ghcr\.io/|docker\.io/|mcr\.microsoft\.com/|[a-zA-Z0-9._-]+\.azurecr\.io/)'
    r'[a-zA-Z0-9._/-]+(:[a-zA-Z0-9._-]+)?$'
)
FEATURE_ID_RE = re.compile(
    r'^ghcr\.io/[a-zA-Z0-9._-]+/[a-zA-Z0-9._/-]+(:[a-zA-Z0-9._-]+)?$'
)


# ---------------------------------------------------------------------------
# JSONC support: strip comments and trailing commas before JSON parse
# ---------------------------------------------------------------------------

def strip_jsonc(text):
    """Remove // and /* */ comments and trailing commas from JSONC text."""
    result = []
    i = 0
    length = len(text)
    in_string = False
    escape = False

    while i < length:
        ch = text[i]

        if in_string:
            result.append(ch)
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        # Not in string
        if ch == '"':
            in_string = True
            result.append(ch)
            i += 1
        elif ch == '/' and i + 1 < length:
            next_ch = text[i + 1]
            if next_ch == '/':
                # Line comment — skip to end of line
                i += 2
                while i < length and text[i] != '\n':
                    i += 1
            elif next_ch == '*':
                # Block comment — skip to */
                i += 2
                while i < length:
                    if text[i] == '*' and i + 1 < length and text[i + 1] == '/':
                        i += 2
                        break
                    i += 1
            else:
                result.append(ch)
                i += 1
        else:
            result.append(ch)
            i += 1

    stripped = "".join(result)
    # Remove trailing commas before } or ]
    stripped = re.sub(r',(\s*[}\]])', r'\1', stripped)
    return stripped


def parse_devcontainer(path):
    """Parse a devcontainer.json (JSONC) file."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    cleaned = strip_jsonc(raw)
    return json.loads(cleaned)


# ---------------------------------------------------------------------------
# Validation categories
# ---------------------------------------------------------------------------

def validate_structure(data, issues):
    """Structure rules (6)."""
    # Empty name
    if "name" in data and (not isinstance(data["name"], str) or not data["name"].strip()):
        issues.append(("error", "empty-name", "'name' is empty or not a string"))

    # Must have at least one of image, dockerFile, dockerComposeFile
    has_image = "image" in data
    has_dockerfile = "dockerFile" in data or ("build" in data and isinstance(data["build"], dict) and "dockerfile" in data["build"])
    has_compose = "dockerComposeFile" in data
    if not has_image and not has_dockerfile and not has_compose:
        issues.append(("error", "missing-image-source",
                        "Must specify at least one of 'image', 'dockerFile', or 'dockerComposeFile'"))

    # Conflicts
    if has_image and ("dockerFile" in data or ("build" in data and isinstance(data.get("build"), dict) and "dockerfile" in data.get("build", {}))):
        issues.append(("error", "image-dockerfile-conflict",
                        "Both 'image' and 'dockerFile'/'build.dockerfile' specified — use one"))
    if "dockerFile" in data and has_compose:
        issues.append(("error", "dockerfile-compose-conflict",
                        "Both 'dockerFile' and 'dockerComposeFile' specified — use one"))

    # Unknown top-level keys
    for key in data:
        if key not in KNOWN_TOP_LEVEL_KEYS:
            # Accept $schema and common meta keys silently
            if key.startswith("$"):
                continue
            issues.append(("warning", "unknown-top-level-key",
                            f"Unknown top-level key '{key}'"))


def validate_features(data, issues):
    """Features rules (4)."""
    features = data.get("features")
    if features is None:
        return

    if not isinstance(features, dict):
        issues.append(("error", "invalid-features-format",
                        "'features' must be an object with string keys"))
        return

    seen_ids = set()
    for feature_id, options in features.items():
        if not isinstance(feature_id, str):
            issues.append(("error", "invalid-feature-id-type",
                            f"Feature key must be a string, got {type(feature_id).__name__}"))
            continue

        # Check valid OCI/ghcr reference
        if not OCI_REF_RE.match(feature_id) and not FEATURE_ID_RE.match(feature_id):
            # Also allow shorthand like ghcr.io/devcontainers/features/go:1
            # or plain feature names from devcontainers spec
            if "/" not in feature_id and ":" not in feature_id:
                issues.append(("warning", "feature-id-not-oci",
                                f"Feature ID '{feature_id}' is not a valid OCI/ghcr.io reference"))

        # Duplicate check (normalize)
        norm = feature_id.lower().split(":")[0]
        if norm in seen_ids:
            issues.append(("error", "duplicate-feature",
                            f"Duplicate feature: '{feature_id}'"))
        seen_ids.add(norm)

        # Empty options warn
        if isinstance(options, dict) and len(options) == 0:
            issues.append(("warning", "empty-feature-options",
                            f"Feature '{feature_id}' has empty options object — use {{}} only if intentional"))


def validate_ports(data, issues):
    """Ports & networking rules (4)."""
    forward_ports = data.get("forwardPorts")
    if forward_ports is not None:
        if not isinstance(forward_ports, list):
            issues.append(("error", "forward-ports-not-array",
                            "'forwardPorts' must be an array"))
        else:
            valid_ports = set()
            for item in forward_ports:
                if isinstance(item, int):
                    if item < 1 or item > 65535:
                        issues.append(("error", "port-out-of-range",
                                        f"Port {item} out of range (1-65535)"))
                    else:
                        valid_ports.add(str(item))
                elif isinstance(item, str):
                    # "host:container" format
                    parts = item.split(":")
                    valid_format = True
                    for part in parts:
                        try:
                            p = int(part)
                            if p < 1 or p > 65535:
                                issues.append(("error", "port-out-of-range",
                                                f"Port {p} in '{item}' out of range (1-65535)"))
                            valid_ports.add(part)
                        except ValueError:
                            issues.append(("error", "invalid-port-number",
                                            f"Invalid port value '{part}' in '{item}' — must be integer or 'host:container' string"))
                            valid_format = False
                else:
                    issues.append(("error", "invalid-port-number",
                                    f"Invalid port entry {item!r} — must be integer or 'host:container' string"))

            # Check portsAttributes references
            ports_attrs = data.get("portsAttributes")
            if isinstance(ports_attrs, dict):
                for port_key in ports_attrs:
                    if port_key not in valid_ports:
                        issues.append(("warning", "ports-attr-unreferenced",
                                        f"portsAttributes references port '{port_key}' not listed in forwardPorts"))


def validate_lifecycle(data, issues):
    """Lifecycle scripts rules (4)."""
    for cmd_key in LIFECYCLE_COMMANDS:
        cmd = data.get(cmd_key)
        if cmd is None:
            continue

        # Validate command type
        if isinstance(cmd, str):
            if not cmd.strip():
                issues.append(("error", "empty-command",
                                f"'{cmd_key}' is an empty string"))
            else:
                _check_shell_injection(cmd, cmd_key, issues)
        elif isinstance(cmd, list):
            if len(cmd) == 0:
                issues.append(("error", "empty-command",
                                f"'{cmd_key}' is an empty array"))
            for item in cmd:
                if not isinstance(item, str):
                    issues.append(("error", "invalid-command-type",
                                    f"'{cmd_key}' array items must be strings, got {type(item).__name__}"))
                elif not item.strip():
                    issues.append(("error", "empty-command",
                                    f"'{cmd_key}' contains an empty string element"))
                else:
                    _check_shell_injection(item, cmd_key, issues)
        elif isinstance(cmd, dict):
            # Parallel commands: object with string keys → string/array values
            if len(cmd) == 0:
                issues.append(("error", "empty-command",
                                f"'{cmd_key}' is an empty object"))
            for sub_name, sub_cmd in cmd.items():
                if isinstance(sub_cmd, str):
                    if not sub_cmd.strip():
                        issues.append(("error", "empty-command",
                                        f"'{cmd_key}.{sub_name}' is an empty string"))
                    else:
                        _check_shell_injection(sub_cmd, f"{cmd_key}.{sub_name}", issues)
                elif isinstance(sub_cmd, list):
                    for item in sub_cmd:
                        if isinstance(item, str):
                            _check_shell_injection(item, f"{cmd_key}.{sub_name}", issues)
                else:
                    issues.append(("error", "invalid-command-type",
                                    f"'{cmd_key}.{sub_name}' must be string or array of strings"))
        else:
            issues.append(("error", "invalid-command-type",
                            f"'{cmd_key}' must be string, array of strings, or object — got {type(cmd).__name__}"))

    # Usage hint: onCreateCommand vs postCreateCommand
    if "onCreateCommand" in data and "postCreateCommand" not in data:
        issues.append(("info", "lifecycle-hint",
                        "Using onCreateCommand without postCreateCommand — postCreateCommand runs after source is available and is more common"))


def _check_shell_injection(cmd_str, context, issues):
    """Warn about suspicious shell patterns."""
    for pattern, desc in SHELL_INJECTION_PATTERNS:
        if re.search(pattern, cmd_str):
            issues.append(("warning", "shell-injection-pattern",
                            f"Suspicious pattern in '{context}': {desc}"))


def validate_customizations(data, issues):
    """Customizations rules (3)."""
    customizations = data.get("customizations")
    if customizations is None:
        return
    if not isinstance(customizations, dict):
        issues.append(("error", "invalid-customizations", "'customizations' must be an object"))
        return

    vscode = customizations.get("vscode")
    if vscode is None:
        return
    if not isinstance(vscode, dict):
        issues.append(("error", "invalid-vscode-customizations", "'customizations.vscode' must be an object"))
        return

    # Extensions
    extensions = vscode.get("extensions")
    if extensions is not None:
        if not isinstance(extensions, list):
            issues.append(("error", "extensions-not-array",
                            "'customizations.vscode.extensions' must be an array of strings"))
        else:
            for ext in extensions:
                if not isinstance(ext, str):
                    issues.append(("error", "extensions-not-array",
                                    f"Extension entry must be a string, got {type(ext).__name__}"))
                elif not EXTENSION_ID_RE.match(ext):
                    issues.append(("warning", "invalid-extension-id",
                                    f"Extension ID '{ext}' doesn't match publisher.name format"))

    # Settings
    settings = vscode.get("settings")
    if settings is not None:
        if not isinstance(settings, dict):
            issues.append(("error", "settings-not-object",
                            "'customizations.vscode.settings' must be an object"))


def validate_best_practices(data, issues):
    """Best practices rules (3+)."""
    if "remoteUser" not in data:
        issues.append(("warning", "missing-remote-user",
                        "No 'remoteUser' specified — container will run as root"))

    if data.get("privileged") is True:
        issues.append(("warning", "privileged-container",
                        "'privileged: true' grants full host access — security risk"))

    if "workspaceFolder" not in data:
        issues.append(("warning", "missing-workspace-folder",
                        "No 'workspaceFolder' specified — defaults may vary across tools"))

    cap_add = data.get("capAdd")
    if isinstance(cap_add, list):
        for cap in cap_add:
            if isinstance(cap, str) and cap in DANGEROUS_CAPS:
                issues.append(("warning", "dangerous-capability",
                                f"capAdd contains '{cap}' — elevated privilege, review if necessary"))


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def validate_all(data):
    """Run all validation rules."""
    issues = []
    validate_structure(data, issues)
    validate_features(data, issues)
    validate_ports(data, issues)
    validate_lifecycle(data, issues)
    validate_customizations(data, issues)
    validate_best_practices(data, issues)
    return issues


def validate_structure_only(data):
    issues = []
    validate_structure(data, issues)
    return issues


def validate_features_only(data):
    issues = []
    validate_features(data, issues)
    return issues


def validate_security_only(data):
    """Security-related rules: privileged, capAdd, shell injection, remoteUser."""
    issues = []
    # remoteUser
    if "remoteUser" not in data:
        issues.append(("warning", "missing-remote-user",
                        "No 'remoteUser' specified — container will run as root"))
    # privileged
    if data.get("privileged") is True:
        issues.append(("warning", "privileged-container",
                        "'privileged: true' grants full host access — security risk"))
    # capAdd
    cap_add = data.get("capAdd")
    if isinstance(cap_add, list):
        for cap in cap_add:
            if isinstance(cap, str) and cap in DANGEROUS_CAPS:
                issues.append(("warning", "dangerous-capability",
                                f"capAdd contains '{cap}' — elevated privilege, review if necessary"))
    # Shell injection in lifecycle commands
    for cmd_key in LIFECYCLE_COMMANDS:
        cmd = data.get(cmd_key)
        if cmd is None:
            continue
        if isinstance(cmd, str):
            _check_shell_injection(cmd, cmd_key, issues)
        elif isinstance(cmd, list):
            for item in cmd:
                if isinstance(item, str):
                    _check_shell_injection(item, cmd_key, issues)
        elif isinstance(cmd, dict):
            for sub_name, sub_cmd in cmd.items():
                if isinstance(sub_cmd, str):
                    _check_shell_injection(sub_cmd, f"{cmd_key}.{sub_name}", issues)
                elif isinstance(sub_cmd, list):
                    for item in sub_cmd:
                        if isinstance(item, str):
                            _check_shell_injection(item, f"{cmd_key}.{sub_name}", issues)
    return issues


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(issues, path):
    if not issues:
        return f"PASS {path}: no issues found"
    icon = "FAIL" if any(s == "error" for s, _, _ in issues) else "WARN"
    lines = [f"{icon} {path}: {len(issues)} issue(s)\n"]
    for severity, rule, msg in sorted(issues, key=lambda x: -SEVERITIES.get(x[0], 0)):
        sev_icon = {"error": "[E]", "warning": "[W]", "info": "[I]"}.get(severity, "[?]")
        lines.append(f"  {sev_icon} {rule}: {msg}")
    return "\n".join(lines)


def format_json(issues, path):
    return json.dumps({
        "file": path,
        "issues": [{"severity": s, "rule": r, "message": m} for s, r, m in issues],
        "summary": {
            "total": len(issues),
            "errors": sum(1 for s, _, _ in issues if s == "error"),
            "warnings": sum(1 for s, _, _ in issues if s == "warning"),
            "info": sum(1 for s, _, _ in issues if s == "info"),
        }
    }, indent=2)


def format_summary(issues, path):
    errs = sum(1 for s, _, _ in issues if s == "error")
    warns = sum(1 for s, _, _ in issues if s == "warning")
    infos = sum(1 for s, _, _ in issues if s == "info")
    status = "FAIL" if errs else ("WARN" if warns else "PASS")
    return f"{status} | {path} | {len(issues)} issues ({errs} errors, {warns} warnings, {infos} info)"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate devcontainer.json files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s validate devcontainer.json
  %(prog)s validate --format json .devcontainer/devcontainer.json
  %(prog)s security --strict devcontainer.json
  %(prog)s structure devcontainer.json
""")

    parser.add_argument("command", choices=["validate", "structure", "features", "security"],
                        help="Validation scope")
    parser.add_argument("file", help="Path to devcontainer.json")
    parser.add_argument("--format", dest="fmt", choices=["text", "json", "summary"],
                        default="text", help="Output format (default: text)")
    parser.add_argument("--min-severity", choices=["error", "warning", "info"],
                        default="info", help="Filter by minimum severity (default: info)")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any issue (including warnings)")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: {args.file} not found", file=sys.stderr)
        sys.exit(2)

    try:
        data = parse_devcontainer(args.file)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON/JSONC syntax in {args.file}: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error parsing {args.file}: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict):
        print(f"Error: {args.file} root must be a JSON object", file=sys.stderr)
        sys.exit(2)

    # Run selected validation
    cmd_map = {
        "validate": validate_all,
        "structure": validate_structure_only,
        "features": validate_features_only,
        "security": validate_security_only,
    }
    issues = cmd_map[args.command](data)

    # Filter by severity
    min_level = SEVERITIES.get(args.min_severity, 1)
    issues = [(s, r, m) for s, r, m in issues if SEVERITIES.get(s, 0) >= min_level]

    # Output
    if args.fmt == "json":
        print(format_json(issues, args.file))
    elif args.fmt == "summary":
        print(format_summary(issues, args.file))
    else:
        print(format_text(issues, args.file))

    # Exit code
    if args.strict and issues:
        sys.exit(1)
    elif any(s == "error" for s, _, _ in issues):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
