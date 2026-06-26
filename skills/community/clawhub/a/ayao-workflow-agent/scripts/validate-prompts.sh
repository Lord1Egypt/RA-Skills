#!/bin/bash
# validate-prompts.sh — Validate prompt template script refs and schema-like fields
# Usage: validate-prompts.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REFERENCES_DIR="$ROOT_DIR/references"
TASK_SCHEMA_FILE="$REFERENCES_DIR/task-schema.md"

python3 - "$ROOT_DIR" "$REFERENCES_DIR" "$TASK_SCHEMA_FILE" <<'PYEOF'
import json
import re
import sys
from pathlib import Path

root_dir = Path(sys.argv[1])
references_dir = Path(sys.argv[2])
task_schema_file = Path(sys.argv[3])

script_ref_re = re.compile(r"(?<![\w./-])(scripts/[A-Za-z0-9._/-]+\.sh)\b")
dollar_ref_re = re.compile(r"(?<!\$)\$([A-Za-z_][A-Za-z0-9_]*)\b")
brace_ref_re = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")

schema_hint_tokens = {
    "agent",
    "attempt",
    "batch",
    "cache",
    "commit",
    "created",
    "depend",
    "domain",
    "input",
    "issue",
    "milestone",
    "name",
    "note",
    "output",
    "project",
    "repo",
    "review",
    "session",
    "status",
    "task",
    "tmux",
    "token",
    "updated",
}

known_field_aliases = {
    "batch_id",
    "project_dir",
    "session",
    "task_id",
    "task_name",
    "workdir",
}

warning_count = 0
error_count = 0
valid_templates = 0


def collect_keys(value, output):
    if isinstance(value, dict):
        for key, nested in value.items():
            output.add(key)
            collect_keys(nested, output)
    elif isinstance(value, list):
        for item in value:
            collect_keys(item, output)


def load_known_fields():
    warnings = []
    fields = set(known_field_aliases)

    if not task_schema_file.exists():
        warnings.append(
            f"⚠️  task-schema.md missing: {task_schema_file} [WARN] "
            "(field validation skipped)"
        )
        return fields, warnings

    try:
        schema_text = task_schema_file.read_text(encoding="utf-8")
    except OSError as exc:
        warnings.append(
            f"⚠️  failed to read {task_schema_file.name}: {exc} [WARN] "
            "(field validation skipped)"
        )
        return fields, warnings

    match = re.search(r"```json\s*(\{.*?\})\s*```", schema_text, re.S)
    if not match:
        warnings.append(
            f"⚠️  {task_schema_file.name} has no JSON schema block [WARN] "
            "(field validation skipped)"
        )
        return fields, warnings

    try:
        schema = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        warnings.append(
            f"⚠️  failed to parse JSON in {task_schema_file.name}: "
            f"{exc.msg} at line {exc.lineno}, column {exc.colno} [WARN] "
            "(field validation skipped)"
        )
        return fields, warnings

    collect_keys(schema, fields)
    return fields, warnings


def is_schema_like(name, known_fields):
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        return False
    if name in known_fields:
        return True

    parts = set(name.split("_"))
    return any(part in schema_hint_tokens for part in parts)


known_fields, schema_warnings = load_known_fields()

print("🔍 Validating prompt templates...")
for warning in schema_warnings:
    print(warning)
warning_count += len(schema_warnings)

if not references_dir.exists():
    print(f"❌ references directory not found: {references_dir} [ERROR]")
    print("结论: 0/0 templates valid, 0 warnings, 1 errors")
    sys.exit(1)

prompt_files = sorted(references_dir.glob("prompt-*.md"))
if not prompt_files:
    print("⚠️  no prompt templates found under references/ [WARN]")
    print("结论: 0/0 templates valid, 1 warnings, 0 errors")
    sys.exit(0)

for prompt_file in prompt_files:
    try:
        content = prompt_file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"❌ {prompt_file.name}: failed to read file ({exc}) [ERROR]")
        error_count += 1
        continue

    missing_scripts = []
    script_refs = sorted(set(script_ref_re.findall(content)))
    for script_ref in script_refs:
        if not (root_dir / script_ref).exists():
            missing_scripts.append(script_ref)

    unknown_fields = []
    for name in sorted(set(dollar_ref_re.findall(content))):
        if is_schema_like(name, known_fields) and name not in known_fields:
            unknown_fields.append(f"${name}")
    for name in sorted(set(brace_ref_re.findall(content))):
        if is_schema_like(name, known_fields) and name not in known_fields:
            unknown_fields.append(f"{{{{{name}}}}}")

    warning_count += len(unknown_fields)
    error_count += len(missing_scripts)

    details = []
    if not missing_scripts:
        details.append("all script references found")
    else:
        details.extend(
            f"references {script_ref} (not found) [ERROR]"
            for script_ref in missing_scripts
        )

    details.extend(
        f"unknown field reference {field_ref} [WARN]"
        for field_ref in unknown_fields
    )

    if missing_scripts:
        print(f"❌ {prompt_file.name}: {'; '.join(details)}")
    elif unknown_fields:
        print(f"⚠️  {prompt_file.name}: {'; '.join(details)}")
        valid_templates += 1
    else:
        print(f"✅ {prompt_file.name}: {'; '.join(details)}")
        valid_templates += 1

print(
    f"结论: {valid_templates}/{len(prompt_files)} templates valid, "
    f"{warning_count} warnings, {error_count} errors"
)
sys.exit(1 if error_count else 0)
PYEOF
