#!/usr/bin/env python3
"""API Diff — compare two OpenAPI/Swagger specs and generate a changelog of breaking/non-breaking changes."""

import argparse
import json
import sys
import os

__version__ = "1.0.0"


def load_spec(path):
    """Load an OpenAPI/Swagger spec from a JSON or YAML file."""
    if not os.path.exists(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Try JSON first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try YAML (basic parser — handles common cases without PyYAML)
    try:
        return _parse_simple_yaml(content)
    except Exception:
        print(f"Error: Could not parse {path} as JSON or YAML", file=sys.stderr)
        sys.exit(1)


def _parse_simple_yaml(content):
    """Minimal YAML-like parser for OpenAPI specs. Handles flat and nested mappings."""
    # For real YAML we'd need PyYAML, but most OpenAPI specs are also available as JSON.
    # This is a best-effort fallback.
    raise ValueError("YAML parsing requires PyYAML. Convert to JSON or install PyYAML.")


def get_spec_version(spec):
    """Detect OpenAPI version."""
    if "openapi" in spec:
        return "openapi3"
    elif "swagger" in spec:
        return "swagger2"
    return "unknown"


def normalize_spec(spec):
    """Normalize spec to a common internal format for comparison."""
    version = get_spec_version(spec)
    result = {
        "info": spec.get("info", {}),
        "paths": {},
        "schemas": {},
        "security": spec.get("security", []),
        "servers": [],
    }

    # Paths
    paths = spec.get("paths", {})
    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        result["paths"][path] = {}
        for method, op in methods.items():
            if method.startswith("x-") or method == "parameters":
                continue
            if not isinstance(op, dict):
                continue
            result["paths"][path][method.upper()] = {
                "summary": op.get("summary", ""),
                "description": op.get("description", ""),
                "parameters": op.get("parameters", []),
                "request_body": op.get("requestBody", {}),
                "responses": op.get("responses", {}),
                "security": op.get("security", None),
                "deprecated": op.get("deprecated", False),
                "tags": op.get("tags", []),
            }

    # Schemas
    if version == "openapi3":
        components = spec.get("components", {})
        result["schemas"] = components.get("schemas", {})
        result["security_schemes"] = components.get("securitySchemes", {})
    elif version == "swagger2":
        result["schemas"] = spec.get("definitions", {})
        result["security_schemes"] = spec.get("securityDefinitions", {})

    # Servers
    if version == "openapi3":
        result["servers"] = spec.get("servers", [])
    elif version == "swagger2":
        host = spec.get("host", "")
        base = spec.get("basePath", "")
        schemes = spec.get("schemes", ["https"])
        if host:
            result["servers"] = [{"url": f"{schemes[0]}://{host}{base}"}]

    return result


def diff_specs(old, new):
    """Compare two normalized specs and return list of changes."""
    changes = []

    def add(change_type, breaking, category, path, detail):
        changes.append({
            "type": change_type,
            "breaking": breaking,
            "category": category,
            "path": path,
            "detail": detail,
        })

    # --- Info changes ---
    old_info = old.get("info", {})
    new_info = new.get("info", {})
    if old_info.get("version") != new_info.get("version"):
        add("changed", False, "info",
            "info.version",
            f"{old_info.get('version', '?')} → {new_info.get('version', '?')}")

    if old_info.get("title") != new_info.get("title"):
        add("changed", False, "info",
            "info.title",
            f"'{old_info.get('title', '')}' → '{new_info.get('title', '')}'")

    # --- Path/endpoint changes ---
    old_paths = old.get("paths", {})
    new_paths = new.get("paths", {})

    all_paths = set(list(old_paths.keys()) + list(new_paths.keys()))

    for path in sorted(all_paths):
        old_methods = old_paths.get(path, {})
        new_methods = new_paths.get(path, {})
        all_methods = set(list(old_methods.keys()) + list(new_methods.keys()))

        for method in sorted(all_methods):
            endpoint = f"{method} {path}"

            if method not in old_methods:
                add("added", False, "endpoint", endpoint, "New endpoint added")
                continue

            if method not in new_methods:
                add("removed", True, "endpoint", endpoint, "Endpoint removed")
                continue

            old_op = old_methods[method]
            new_op = new_methods[method]

            # Deprecated
            if not old_op.get("deprecated") and new_op.get("deprecated"):
                add("deprecated", False, "endpoint", endpoint, "Endpoint deprecated")
            elif old_op.get("deprecated") and not new_op.get("deprecated"):
                add("changed", False, "endpoint", endpoint, "Deprecation removed")

            # Parameters
            old_params = {_param_key(p): p for p in old_op.get("parameters", [])}
            new_params = {_param_key(p): p for p in new_op.get("parameters", [])}

            for key in old_params:
                if key not in new_params:
                    p = old_params[key]
                    if p.get("required"):
                        add("removed", True, "parameter",
                            f"{endpoint} → param '{p.get('name', key)}'",
                            "Required parameter removed")
                    else:
                        add("removed", False, "parameter",
                            f"{endpoint} → param '{p.get('name', key)}'",
                            "Optional parameter removed")

            for key in new_params:
                if key not in old_params:
                    p = new_params[key]
                    if p.get("required"):
                        add("added", True, "parameter",
                            f"{endpoint} → param '{p.get('name', key)}'",
                            "New required parameter added (breaking for existing clients)")
                    else:
                        add("added", False, "parameter",
                            f"{endpoint} → param '{p.get('name', key)}'",
                            "New optional parameter added")

            # Parameter type changes
            for key in old_params:
                if key in new_params:
                    old_type = _get_param_type(old_params[key])
                    new_type = _get_param_type(new_params[key])
                    if old_type != new_type:
                        add("changed", True, "parameter",
                            f"{endpoint} → param '{old_params[key].get('name', key)}'",
                            f"Type changed: {old_type} → {new_type}")

                    # Required changed
                    old_req = old_params[key].get("required", False)
                    new_req = new_params[key].get("required", False)
                    if not old_req and new_req:
                        add("changed", True, "parameter",
                            f"{endpoint} → param '{old_params[key].get('name', key)}'",
                            "Parameter became required")
                    elif old_req and not new_req:
                        add("changed", False, "parameter",
                            f"{endpoint} → param '{old_params[key].get('name', key)}'",
                            "Parameter became optional")

            # Response changes
            old_resp = old_op.get("responses", {})
            new_resp = new_op.get("responses", {})

            for code in old_resp:
                if code not in new_resp:
                    add("removed", True, "response",
                        f"{endpoint} → response {code}",
                        "Response code removed")

            for code in new_resp:
                if code not in old_resp:
                    add("added", False, "response",
                        f"{endpoint} → response {code}",
                        "New response code added")

            # Security changes
            old_sec = old_op.get("security")
            new_sec = new_op.get("security")
            if old_sec != new_sec and old_sec is not None and new_sec is not None:
                add("changed", True, "security",
                    f"{endpoint} → security",
                    "Security requirements changed")

    # --- Schema changes ---
    old_schemas = old.get("schemas", {})
    new_schemas = new.get("schemas", {})

    for name in old_schemas:
        if name not in new_schemas:
            add("removed", True, "schema", f"schema/{name}", "Schema removed")

    for name in new_schemas:
        if name not in old_schemas:
            add("added", False, "schema", f"schema/{name}", "New schema added")

    for name in old_schemas:
        if name in new_schemas:
            schema_changes = _diff_schema(old_schemas[name], new_schemas[name], f"schema/{name}")
            changes.extend(schema_changes)

    # --- Server changes ---
    old_servers = [s.get("url", "") for s in old.get("servers", [])]
    new_servers = [s.get("url", "") for s in new.get("servers", [])]
    if old_servers != new_servers:
        add("changed", False, "server", "servers",
            f"Server URLs changed: {old_servers} → {new_servers}")

    return changes


def _param_key(param):
    return f"{param.get('name', '')}:{param.get('in', '')}"


def _get_param_type(param):
    schema = param.get("schema", {})
    if schema:
        return schema.get("type", "unknown")
    return param.get("type", "unknown")


def _diff_schema(old_schema, new_schema, prefix):
    """Compare two schema objects, return list of changes."""
    changes = []

    def add(change_type, breaking, detail):
        changes.append({
            "type": change_type,
            "breaking": breaking,
            "category": "schema",
            "path": prefix,
            "detail": detail,
        })

    old_type = old_schema.get("type", "")
    new_type = new_schema.get("type", "")
    if old_type != new_type and old_type and new_type:
        add("changed", True, f"Type changed: {old_type} → {new_type}")

    # Properties
    old_props = old_schema.get("properties", {})
    new_props = new_schema.get("properties", {})
    old_required = set(old_schema.get("required", []))
    new_required = set(new_schema.get("required", []))

    for prop in old_props:
        if prop not in new_props:
            add("removed", True, f"Property '{prop}' removed")

    for prop in new_props:
        if prop not in old_props:
            if prop in new_required:
                add("added", True, f"New required property '{prop}' added")
            else:
                add("added", False, f"New optional property '{prop}' added")

    for prop in old_props:
        if prop in new_props:
            old_pt = old_props[prop].get("type", "")
            new_pt = new_props[prop].get("type", "")
            if old_pt != new_pt and old_pt and new_pt:
                add("changed", True, f"Property '{prop}' type: {old_pt} → {new_pt}")

    # Required changes
    newly_required = new_required - old_required
    for prop in newly_required:
        if prop in old_props:
            add("changed", True, f"Property '{prop}' became required")

    newly_optional = old_required - new_required
    for prop in newly_optional:
        if prop in new_props:
            add("changed", False, f"Property '{prop}' became optional")

    # Enum changes
    old_enum = old_schema.get("enum", [])
    new_enum = new_schema.get("enum", [])
    if old_enum and new_enum:
        removed_values = set(str(v) for v in old_enum) - set(str(v) for v in new_enum)
        added_values = set(str(v) for v in new_enum) - set(str(v) for v in old_enum)
        if removed_values:
            add("changed", True, f"Enum values removed: {', '.join(sorted(removed_values))}")
        if added_values:
            add("changed", False, f"Enum values added: {', '.join(sorted(added_values))}")

    return changes


def summarize(changes):
    """Generate summary stats from changes."""
    breaking = [c for c in changes if c["breaking"]]
    non_breaking = [c for c in changes if not c["breaking"]]

    categories = {}
    for c in changes:
        cat = c["category"]
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total": len(changes),
        "breaking": len(breaking),
        "non_breaking": len(non_breaking),
        "by_category": categories,
        "by_type": {
            "added": len([c for c in changes if c["type"] == "added"]),
            "removed": len([c for c in changes if c["type"] == "removed"]),
            "changed": len([c for c in changes if c["type"] == "changed"]),
            "deprecated": len([c for c in changes if c["type"] == "deprecated"]),
        }
    }


def format_text(old_path, new_path, changes, summary):
    lines = []
    lines.append(f"API Diff: {old_path} → {new_path}")
    lines.append(f"Changes: {summary['total']} ({summary['breaking']} breaking, {summary['non_breaking']} non-breaking)")
    lines.append("=" * 60)

    if not changes:
        lines.append("\nNo changes detected.")
        return "\n".join(lines)

    # Breaking changes first
    breaking = [c for c in changes if c["breaking"]]
    non_breaking = [c for c in changes if not c["breaking"]]

    if breaking:
        lines.append("\n⚠️  BREAKING CHANGES")
        lines.append("-" * 40)
        for c in breaking:
            icon = {"added": "➕", "removed": "➖", "changed": "🔄", "deprecated": "⚡"}.get(c["type"], "•")
            lines.append(f"  {icon} [{c['category']}] {c['path']}")
            lines.append(f"    {c['detail']}")

    if non_breaking:
        lines.append("\n✅ NON-BREAKING CHANGES")
        lines.append("-" * 40)
        for c in non_breaking:
            icon = {"added": "➕", "removed": "➖", "changed": "🔄", "deprecated": "⚡"}.get(c["type"], "•")
            lines.append(f"  {icon} [{c['category']}] {c['path']}")
            lines.append(f"    {c['detail']}")

    lines.append("")
    return "\n".join(lines)


def format_json(old_path, new_path, changes, summary):
    return json.dumps({
        "old_spec": old_path,
        "new_spec": new_path,
        "summary": summary,
        "changes": changes,
    }, indent=2)


def format_markdown(old_path, new_path, changes, summary):
    lines = []
    lines.append(f"# API Changelog")
    lines.append(f"\n**Comparing:** `{old_path}` → `{new_path}`")
    lines.append(f"\n**Total changes:** {summary['total']} ({summary['breaking']} breaking, {summary['non_breaking']} non-breaking)")

    if not changes:
        lines.append("\nNo changes detected.")
        return "\n".join(lines)

    breaking = [c for c in changes if c["breaking"]]
    non_breaking = [c for c in changes if not c["breaking"]]

    if breaking:
        lines.append("\n## ⚠️ Breaking Changes\n")
        for c in breaking:
            lines.append(f"- **{c['path']}** — {c['detail']}")

    if non_breaking:
        lines.append("\n## ✅ Non-Breaking Changes\n")
        for c in non_breaking:
            lines.append(f"- **{c['path']}** — {c['detail']}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="API Diff — compare OpenAPI/Swagger specs and generate changelogs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 api_diff.py old-api.json new-api.json
  python3 api_diff.py v1.json v2.json --format markdown
  python3 api_diff.py v1.json v2.json --breaking-only
  python3 api_diff.py v1.json v2.json --fail-on-breaking""")

    parser.add_argument("old_spec", help="Path to old/baseline API spec (JSON)")
    parser.add_argument("new_spec", help="Path to new/updated API spec (JSON)")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--breaking-only", action="store_true", help="Show only breaking changes")
    parser.add_argument("--fail-on-breaking", action="store_true",
                        help="Exit with code 1 if breaking changes found")
    parser.add_argument("--version", action="version", version=f"api-diff {__version__}")

    args = parser.parse_args()

    old_spec = normalize_spec(load_spec(args.old_spec))
    new_spec = normalize_spec(load_spec(args.new_spec))

    changes = diff_specs(old_spec, new_spec)

    if args.breaking_only:
        changes = [c for c in changes if c["breaking"]]

    summary = summarize(changes)

    if args.format == "json":
        print(format_json(args.old_spec, args.new_spec, changes, summary))
    elif args.format == "markdown":
        print(format_markdown(args.old_spec, args.new_spec, changes, summary))
    else:
        print(format_text(args.old_spec, args.new_spec, changes, summary))

    if args.fail_on_breaking and summary["breaking"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
