#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# fixture — Test Data Fixture Generator
# Version: 1.0.0
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
###############################################################################

DATA_DIR="$HOME/.fixture"
DATA_FILE="$DATA_DIR/data.jsonl"
TEMPLATES_FILE="$DATA_DIR/templates.json"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"
[[ -f "$TEMPLATES_FILE" ]] || echo '{}' > "$TEMPLATES_FILE"

COMMAND="${1:-help}"
shift 2>/dev/null || true

case "$COMMAND" in

create)
  NAME="" TYPE="" FIELDS=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name) NAME="$2"; shift 2;;
      --type) TYPE="$2"; shift 2;;
      --fields) FIELDS="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$NAME" || -z "$TYPE" || -z "$FIELDS" ]]; then
    echo "Error: --name, --type, and --fields are required"
    exit 1
  fi
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_NAME="$NAME"
  export FIXTURE_TYPE="$TYPE"
  export FIXTURE_FIELDS="$FIELDS"
  python3 << 'PYEOF'
import json, os, uuid, time

data_file = os.environ["FIXTURE_DATA_FILE"]
name = os.environ["FIXTURE_NAME"]
ftype = os.environ["FIXTURE_TYPE"]
fields = json.loads(os.environ["FIXTURE_FIELDS"])

record = {
    "id": str(uuid.uuid4())[:8],
    "name": name,
    "type": ftype,
    "fields": fields,
    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
}

with open(data_file, "a") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"✅ Fixture created: {record['id']}")
print(f"   Name: {name}")
print(f"   Type: {ftype}")
print(f"   Fields: {json.dumps(fields, ensure_ascii=False)}")
PYEOF
  ;;

load)
  FILE="" FORMAT=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file) FILE="$2"; shift 2;;
      --format) FORMAT="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$FILE" ]]; then
    echo "Error: --file is required"
    exit 1
  fi
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_INPUT_FILE="$FILE"
  export FIXTURE_FORMAT="$FORMAT"
  python3 << 'PYEOF'
import json, os, uuid, time

data_file = os.environ["FIXTURE_DATA_FILE"]
input_file = os.environ["FIXTURE_INPUT_FILE"]
fmt = os.environ.get("FIXTURE_FORMAT", "")

if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    exit(1)

if not fmt:
    fmt = "jsonl" if input_file.endswith(".jsonl") else "json"

count = 0
with open(input_file) as inf:
    if fmt == "jsonl":
        entries = [json.loads(line.strip()) for line in inf if line.strip()]
    else:
        entries = json.load(inf)
        if isinstance(entries, dict):
            entries = [entries]

with open(data_file, "a") as f:
    for entry in entries:
        if "id" not in entry:
            entry["id"] = str(uuid.uuid4())[:8]
        if "created_at" not in entry:
            entry["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        count += 1

print(f"✅ Loaded {count} fixtures from {input_file}")
PYEOF
  ;;

dump)
  TYPE="" OUTPUT=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --type) TYPE="$2"; shift 2;;
      --output) OUTPUT="$2"; shift 2;;
      *) shift;;
    esac
  done
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_TYPE="$TYPE"
  export FIXTURE_OUTPUT="$OUTPUT"
  python3 << 'PYEOF'
import json, os, sys

data_file = os.environ["FIXTURE_DATA_FILE"]
ftype = os.environ.get("FIXTURE_TYPE", "")
output = os.environ.get("FIXTURE_OUTPUT", "")

entries = []
if os.path.exists(data_file):
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                if not ftype or e.get("type") == ftype:
                    entries.append(e)

result = json.dumps(entries, indent=2, ensure_ascii=False)

if output:
    with open(output, "w") as f:
        f.write(result)
    print(f"✅ Dumped {len(entries)} fixtures to {output}")
else:
    print(result)
PYEOF
  ;;

list)
  TYPE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --type) TYPE="$2"; shift 2;;
      *) shift;;
    esac
  done
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_TYPE="$TYPE"
  python3 << 'PYEOF'
import json, os
from collections import Counter

data_file = os.environ["FIXTURE_DATA_FILE"]
ftype = os.environ.get("FIXTURE_TYPE", "")

entries = []
if os.path.exists(data_file):
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                if not ftype or e.get("type") == ftype:
                    entries.append(e)

if not entries:
    print("📋 No fixtures found.")
    exit(0)

types = Counter(e.get("type", "unknown") for e in entries)
print(f"📋 Fixtures ({len(entries)} total)")
print(f"   Types: {dict(types)}\n")

for e in entries[:20]:
    fields_summary = list(e.get("fields", {}).keys()) if isinstance(e.get("fields"), dict) else []
    print(f"  [{e.get('id','')}] {e.get('name','')} ({e.get('type','')}) — {', '.join(fields_summary[:4])}")

if len(entries) > 20:
    print(f"\n   ... and {len(entries) - 20} more")
PYEOF
  ;;

seed)
  TEMPLATE="" COUNT="" SEED=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --template) TEMPLATE="$2"; shift 2;;
      --count) COUNT="$2"; shift 2;;
      --seed) SEED="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$TEMPLATE" || -z "$COUNT" ]]; then
    echo "Error: --template and --count are required"
    exit 1
  fi
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_TEMPLATES_FILE="$TEMPLATES_FILE"
  export FIXTURE_TEMPLATE="$TEMPLATE"
  export FIXTURE_COUNT="$COUNT"
  export FIXTURE_SEED="${SEED:-}"
  python3 << 'PYEOF'
import json, os, uuid, time, random, string

data_file = os.environ["FIXTURE_DATA_FILE"]
templates_file = os.environ["FIXTURE_TEMPLATES_FILE"]
template_name = os.environ["FIXTURE_TEMPLATE"]
count = int(os.environ["FIXTURE_COUNT"])
seed_val = os.environ.get("FIXTURE_SEED", "")

if seed_val:
    random.seed(int(seed_val))

with open(templates_file) as f:
    templates = json.load(f)

if template_name not in templates:
    print(f"❌ Template not found: {template_name}")
    print(f"   Available: {', '.join(templates.keys()) if templates else 'none'}")
    exit(1)

schema = templates[template_name]
first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Moore"]
domains = ["test.com", "example.org", "mock.dev", "fixture.io"]

def generate_value(field_type):
    if field_type == "string":
        return ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 15)))
    elif field_type == "email":
        name = random.choice(first_names).lower()
        return f"{name}{random.randint(1,999)}@{random.choice(domains)}"
    elif field_type.startswith("int:"):
        lo, hi = field_type[4:].split("-")
        return random.randint(int(lo), int(hi))
    elif field_type.startswith("float:"):
        lo, hi = field_type[6:].split("-")
        return round(random.uniform(float(lo), float(hi)), 2)
    elif field_type == "bool":
        return random.choice([True, False])
    elif field_type == "uuid":
        return str(uuid.uuid4())
    elif field_type == "date":
        year = random.randint(2020, 2026)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"
    elif field_type == "name":
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    else:
        return field_type

generated = 0
with open(data_file, "a") as f:
    for i in range(count):
        fields = {}
        for field_name, field_type in schema.items():
            fields[field_name] = generate_value(field_type)
        record = {
            "id": str(uuid.uuid4())[:8],
            "name": f"{template_name}_{i+1}",
            "type": template_name,
            "fields": fields,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "seeded": True
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        generated += 1

print(f"✅ Generated {generated} fixtures from template '{template_name}'")
if seed_val:
    print(f"   Seed: {seed_val} (reproducible)")
PYEOF
  ;;

reset)
  TYPE="" CONFIRM=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --type) TYPE="$2"; shift 2;;
      --confirm) CONFIRM="1"; shift;;
      *) shift;;
    esac
  done
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_TYPE="$TYPE"
  export FIXTURE_CONFIRM="$CONFIRM"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FIXTURE_DATA_FILE"]
ftype = os.environ.get("FIXTURE_TYPE", "")
confirm = os.environ.get("FIXTURE_CONFIRM", "") == "1"

if not os.path.exists(data_file):
    print("📋 No data to reset.")
    exit(0)

if ftype:
    keep = []
    removed = 0
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                if e.get("type") == ftype:
                    removed += 1
                else:
                    keep.append(line)
    with open(data_file, "w") as f:
        for line in keep:
            f.write(line + "\n")
    print(f"✅ Removed {removed} fixtures of type '{ftype}'")
    print(f"   Remaining: {len(keep)}")
else:
    if not confirm:
        with open(data_file) as f:
            count = sum(1 for line in f if line.strip())
        print(f"⚠️  This will delete ALL {count} fixtures.")
        print(f"   Run with --confirm to proceed.")
        exit(0)
    open(data_file, "w").close()
    print("✅ All fixtures have been reset.")
PYEOF
  ;;

template)
  LIST="" CREATE="" SCHEMA="" SHOW=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --list) LIST="1"; shift;;
      --create) CREATE="$2"; shift 2;;
      --schema) SCHEMA="$2"; shift 2;;
      --show) SHOW="$2"; shift 2;;
      *) shift;;
    esac
  done
  export FIXTURE_TEMPLATES_FILE="$TEMPLATES_FILE"
  export FIXTURE_LIST="$LIST"
  export FIXTURE_CREATE="$CREATE"
  export FIXTURE_SCHEMA="$SCHEMA"
  export FIXTURE_SHOW="$SHOW"
  python3 << 'PYEOF'
import json, os

templates_file = os.environ["FIXTURE_TEMPLATES_FILE"]
do_list = os.environ.get("FIXTURE_LIST", "") == "1"
create = os.environ.get("FIXTURE_CREATE", "")
schema = os.environ.get("FIXTURE_SCHEMA", "")
show = os.environ.get("FIXTURE_SHOW", "")

with open(templates_file) as f:
    templates = json.load(f)

if do_list:
    if not templates:
        print("📋 No templates defined.")
    else:
        print(f"📋 Templates ({len(templates)}):")
        for name, fields in templates.items():
            print(f"   {name}: {', '.join(f'{k}({v})' for k, v in fields.items())}")
elif show:
    if show in templates:
        print(f"📋 Template: {show}")
        print(json.dumps(templates[show], indent=2))
    else:
        print(f"❌ Template not found: {show}")
elif create and schema:
    templates[create] = json.loads(schema)
    with open(templates_file, "w") as f:
        json.dump(templates, f, indent=2)
    print(f"✅ Template created: {create}")
    print(f"   Schema: {schema}")
else:
    print("Usage: template --list | --create <name> --schema '<json>' | --show <name>")
PYEOF
  ;;

validate)
  TYPE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --type) TYPE="$2"; shift 2;;
      *) shift;;
    esac
  done
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_TEMPLATES_FILE="$TEMPLATES_FILE"
  export FIXTURE_TYPE="$TYPE"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FIXTURE_DATA_FILE"]
templates_file = os.environ["FIXTURE_TEMPLATES_FILE"]
ftype = os.environ.get("FIXTURE_TYPE", "")

with open(templates_file) as f:
    templates = json.load(f)

entries = []
if os.path.exists(data_file):
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                if not ftype or e.get("type") == ftype:
                    entries.append(e)

if not entries:
    print("⚠️  No fixtures to validate.")
    exit(0)

errors = []
warnings = []
for e in entries:
    etype = e.get("type", "")
    if etype in templates:
        schema = templates[etype]
        fields = e.get("fields", {})
        for field_name in schema:
            if field_name not in fields:
                errors.append(f"Entry {e['id']}: Missing field '{field_name}'")
        for field_name in fields:
            if field_name not in schema:
                warnings.append(f"Entry {e['id']}: Extra field '{field_name}'")
    else:
        warnings.append(f"Entry {e['id']}: No template for type '{etype}'")

    if not e.get("id"):
        errors.append(f"Entry missing ID")
    if not e.get("fields"):
        errors.append(f"Entry {e.get('id','?')}: Empty fields")

print(f"📊 Validation ({len(entries)} fixtures)")
print(f"   Errors: {len(errors)}")
print(f"   Warnings: {len(warnings)}")
if errors:
    print("\n❌ Errors:")
    for err in errors[:15]:
        print(f"   • {err}")
if warnings:
    print("\n⚠️  Warnings:")
    for w in warnings[:15]:
        print(f"   • {w}")
if not errors and not warnings:
    print("✅ All fixtures valid!")
PYEOF
  ;;

export)
  OUTPUT="" FORMAT=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --output) OUTPUT="$2"; shift 2;;
      --format) FORMAT="$2"; shift 2;;
      --table) export FIXTURE_TABLE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$OUTPUT" || -z "$FORMAT" ]]; then
    echo "Error: --output and --format are required"
    exit 1
  fi
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_OUTPUT="$OUTPUT"
  export FIXTURE_FORMAT="$FORMAT"
  python3 << 'PYEOF'
import json, os, csv

data_file = os.environ["FIXTURE_DATA_FILE"]
output = os.environ["FIXTURE_OUTPUT"]
fmt = os.environ["FIXTURE_FORMAT"]
table = os.environ.get("FIXTURE_TABLE", "fixtures")

entries = []
if os.path.exists(data_file):
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

if not entries:
    print("⚠️  No fixtures to export.")
    exit(0)

with open(output, "w") as f:
    if fmt == "json":
        json.dump(entries, f, indent=2, ensure_ascii=False)
    elif fmt == "jsonl":
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    elif fmt == "csv":
        all_keys = set()
        for e in entries:
            if isinstance(e.get("fields"), dict):
                all_keys.update(e["fields"].keys())
        all_keys = sorted(all_keys)
        writer = csv.writer(f)
        writer.writerow(["id", "name", "type"] + list(all_keys))
        for e in entries:
            fields = e.get("fields", {})
            row = [e.get("id",""), e.get("name",""), e.get("type","")]
            row += [fields.get(k, "") for k in all_keys]
            writer.writerow(row)
    elif fmt == "sql":
        for e in entries:
            fields = e.get("fields", {})
            if fields:
                cols = ", ".join(fields.keys())
                vals = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in fields.values())
                f.write(f"INSERT INTO {table} ({cols}) VALUES ({vals});\n")

print(f"✅ Exported {len(entries)} fixtures to {output} (format: {fmt})")
PYEOF
  ;;

import)
  FILE="" TYPE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file) FILE="$2"; shift 2;;
      --type) TYPE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$FILE" || -z "$TYPE" ]]; then
    echo "Error: --file and --type are required"
    exit 1
  fi
  export FIXTURE_DATA_FILE="$DATA_FILE"
  export FIXTURE_INPUT_FILE="$FILE"
  export FIXTURE_TYPE="$TYPE"
  python3 << 'PYEOF'
import json, os, uuid, time, csv

data_file = os.environ["FIXTURE_DATA_FILE"]
input_file = os.environ["FIXTURE_INPUT_FILE"]
ftype = os.environ["FIXTURE_TYPE"]

if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    exit(1)

count = 0
with open(data_file, "a") as out:
    if input_file.endswith(".csv"):
        with open(input_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = {
                    "id": str(uuid.uuid4())[:8],
                    "name": f"{ftype}_{count+1}",
                    "type": ftype,
                    "fields": dict(row),
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "imported": True
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
    elif input_file.endswith(".jsonl"):
        with open(input_file) as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    record = {
                        "id": str(uuid.uuid4())[:8],
                        "name": f"{ftype}_{count+1}",
                        "type": ftype,
                        "fields": data if isinstance(data, dict) else {"value": data},
                        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "imported": True
                    }
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    count += 1
    else:
        with open(input_file) as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    record = {
                        "id": str(uuid.uuid4())[:8],
                        "name": f"{ftype}_{count+1}",
                        "type": ftype,
                        "fields": item if isinstance(item, dict) else {"value": item},
                        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "imported": True
                    }
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    count += 1

print(f"✅ Imported {count} records as type '{ftype}'")
PYEOF
  ;;

help)
  cat << 'HELPEOF'
fixture — Test Data Fixture Generator v1.0.0

Commands:
  create      Create a new fixture record
  load        Load fixtures from a file
  dump        Dump fixtures to stdout or file
  list        List all fixtures
  seed        Generate fixtures from template
  reset       Clear fixture data
  template    Manage fixture templates
  validate    Validate fixtures against schema
  export      Export fixtures to various formats
  import      Import fixtures from external files
  help        Show this help message
  version     Show version

Usage: bash scripts/script.sh <command> [options]

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
  ;;

version)
  echo "fixture v1.0.0"
  ;;

*)
  echo "Unknown command: $COMMAND"
  echo "Run 'bash scripts/script.sh help' for usage."
  exit 1
  ;;

esac
