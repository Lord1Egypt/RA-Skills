#!/usr/bin/env bash
# cache/scripts/script.sh — Local Key-Value Cache Manager
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail

VERSION="1.0.0"
DATA_DIR="$HOME/.cache-tool"
DATA_FILE="$DATA_DIR/data.jsonl"
CONFIG_FILE="$DATA_DIR/config.json"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

if [ ! -f "$CONFIG_FILE" ]; then
  echo '{"default_ttl":3600,"max_entries":10000}' > "$CONFIG_FILE"
fi

COMMAND="${1:-help}"
shift 2>/dev/null || true

export DATA_FILE CONFIG_FILE
export ARGS="$*"

show_help() {
  cat << 'EOF'
Cache — Local Key-Value Cache Manager v1.0.0

Usage: bash script.sh <command> [options]

Commands:
  set       Store a key-value pair with optional TTL and tags
  get       Retrieve value for a key
  delete    Remove a key from cache
  list      List all cache entries
  flush     Delete all or matching entries
  ttl       Check or update TTL for a key
  stats     Show cache statistics
  export    Export cache to JSON file
  import    Import cache from JSON file
  search    Search keys/values by pattern
  config    View or update settings
  help      Show this help message
  version   Print version

Options:
  --key       Cache key
  --value     Cache value (string or JSON)
  --ttl       Time-to-live in seconds
  --tags      Comma-separated tags
  --tag       Filter by tag
  --pattern   Glob pattern for flush
  --query     Search query
  --field     Search field: key, value, or both
  --output    Output file path
  --input     Input file path
  --set       Config key=value
EOF
}

case "$COMMAND" in
  set)
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE")
config_file = os.environ.get("CONFIG_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

key = params.get("key", "")
if not key:
    print(json.dumps({"error": "Please provide --key"}, indent=2))
    exit(1)

value = params.get("value", "")
tags_raw = params.get("tags", "")
tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []

with open(config_file, "r") as f:
    config = json.load(f)

ttl = int(params.get("ttl", str(config.get("default_ttl", 3600))))
now = datetime.datetime.utcnow()
expires = now + datetime.timedelta(seconds=ttl)

# Remove existing key if present
records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("key") != key:
            records.append(rec)

# Add new entry
new_record = {
    "key": key,
    "value": value,
    "ttl": ttl,
    "tags": tags,
    "created_at": now.isoformat() + "Z",
    "expires_at": expires.isoformat() + "Z",
    "access_count": 0,
    "last_accessed": None
}
records.append(new_record)

with open(data_file, "w") as f:
    for rec in records:
        f.write(json.dumps(rec) + "\n")

print(json.dumps({"status": "set", "key": key, "ttl": ttl, "expires_at": expires.isoformat() + "Z"}, indent=2))
PYEOF
    ;;

  get)
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

key = params.get("key", "")
if not key:
    print(json.dumps({"error": "Please provide --key"}, indent=2))
    exit(1)

now = datetime.datetime.utcnow()
records = []
found_value = None
found = False

with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("key") == key:
            exp = rec.get("expires_at", "")
            try:
                exp_dt = datetime.datetime.fromisoformat(exp.replace("Z", ""))
                if now > exp_dt:
                    # Expired — skip
                    continue
            except:
                pass
            found = True
            rec["access_count"] = rec.get("access_count", 0) + 1
            rec["last_accessed"] = now.isoformat() + "Z"
            found_value = rec.get("value", "")
        records.append(rec)

if found:
    # Update access count
    with open(data_file, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    # Output raw value
    print(found_value)
else:
    print(json.dumps({"error": f"Key '{key}' not found or expired"}, indent=2))
    exit(1)
PYEOF
    ;;

  delete)
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

key = params.get("key", "")
if not key:
    print(json.dumps({"error": "Please provide --key"}, indent=2))
    exit(1)

records = []
deleted = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("key") == key:
            deleted = True
        else:
            records.append(rec)

with open(data_file, "w") as f:
    for rec in records:
        f.write(json.dumps(rec) + "\n")

if deleted:
    print(json.dumps({"status": "deleted", "key": key}, indent=2))
else:
    print(json.dumps({"error": f"Key '{key}' not found"}, indent=2))
PYEOF
    ;;

  list)
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

tag_filter = params.get("tag", "")
now = datetime.datetime.utcnow()

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)

        # Check expiry
        exp = rec.get("expires_at", "")
        try:
            exp_dt = datetime.datetime.fromisoformat(exp.replace("Z", ""))
            is_expired = now > exp_dt
        except:
            is_expired = False

        status = "expired" if is_expired else "active"

        if tag_filter and tag_filter not in rec.get("tags", []):
            continue

        records.append({
            "key": rec.get("key"),
            "status": status,
            "ttl": rec.get("ttl"),
            "tags": rec.get("tags", []),
            "created_at": rec.get("created_at"),
            "expires_at": rec.get("expires_at"),
            "access_count": rec.get("access_count", 0)
        })

if records:
    print(json.dumps(records, indent=2))
else:
    print(json.dumps({"message": "Cache is empty"}, indent=2))
PYEOF
    ;;

  flush)
    python3 << 'PYEOF'
import json, os, re, fnmatch

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

pattern = params.get("pattern", "")

if not pattern:
    # Flush everything
    with open(data_file, "w") as f:
        pass
    print(json.dumps({"status": "flushed", "message": "All entries deleted"}, indent=2))
else:
    records = []
    flushed = 0
    with open(data_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if fnmatch.fnmatch(rec.get("key", ""), pattern):
                flushed += 1
            else:
                records.append(rec)

    with open(data_file, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    print(json.dumps({"status": "flushed", "pattern": pattern, "deleted_count": flushed}, indent=2))
PYEOF
    ;;

  ttl)
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

key = params.get("key", "")
new_ttl = params.get("set", "")

if not key:
    print(json.dumps({"error": "Please provide --key"}, indent=2))
    exit(1)

now = datetime.datetime.utcnow()
records = []
found = False

with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("key") == key:
            found = True
            if new_ttl:
                new_ttl_int = int(new_ttl)
                rec["ttl"] = new_ttl_int
                rec["expires_at"] = (now + datetime.timedelta(seconds=new_ttl_int)).isoformat() + "Z"
                print(json.dumps({"status": "updated", "key": key, "new_ttl": new_ttl_int, "expires_at": rec["expires_at"]}, indent=2))
            else:
                exp = rec.get("expires_at", "")
                try:
                    exp_dt = datetime.datetime.fromisoformat(exp.replace("Z", ""))
                    remaining = max(0, int((exp_dt - now).total_seconds()))
                except:
                    remaining = -1
                print(json.dumps({"key": key, "ttl_total": rec.get("ttl"), "ttl_remaining": remaining}, indent=2))
        records.append(rec)

if not found:
    print(json.dumps({"error": f"Key '{key}' not found"}, indent=2))
    exit(1)

if new_ttl:
    with open(data_file, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
PYEOF
    ;;

  stats)
    python3 << 'PYEOF'
import json, os, datetime

data_file = os.environ.get("DATA_FILE")
now = datetime.datetime.utcnow()

total = 0
active = 0
expired = 0
total_access = 0
total_bytes = 0
tags_set = set()

with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        total += 1
        total_access += rec.get("access_count", 0)
        total_bytes += len(json.dumps(rec))
        for t in rec.get("tags", []):
            tags_set.add(t)

        exp = rec.get("expires_at", "")
        try:
            exp_dt = datetime.datetime.fromisoformat(exp.replace("Z", ""))
            if now > exp_dt:
                expired += 1
            else:
                active += 1
        except:
            active += 1

print(json.dumps({
    "total_entries": total,
    "active": active,
    "expired": expired,
    "total_accesses": total_access,
    "data_size_bytes": total_bytes,
    "data_size_kb": round(total_bytes / 1024, 2),
    "unique_tags": sorted(list(tags_set))
}, indent=2))
PYEOF
    ;;

  export)
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

output = params.get("output", "")

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

if output:
    with open(output, "w") as f:
        json.dump(records, f, indent=2)
    print(json.dumps({"status": "exported", "file": output, "count": len(records)}, indent=2))
else:
    print(json.dumps(records, indent=2))
PYEOF
    ;;

  import)
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

input_file = params.get("input", "")
if not input_file:
    print(json.dumps({"error": "Please provide --input"}, indent=2))
    exit(1)

if not os.path.exists(input_file):
    print(json.dumps({"error": f"File not found: {input_file}"}, indent=2))
    exit(1)

with open(input_file, "r") as f:
    import_data = json.load(f)

if not isinstance(import_data, list):
    import_data = [import_data]

# Load existing and merge
existing = {}
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        existing[rec.get("key")] = rec

imported = 0
updated = 0
for rec in import_data:
    key = rec.get("key", "")
    if not key:
        continue
    if key in existing:
        updated += 1
    else:
        imported += 1
    existing[key] = rec

with open(data_file, "w") as f:
    for rec in existing.values():
        f.write(json.dumps(rec) + "\n")

print(json.dumps({"status": "imported", "new": imported, "updated": updated, "total": len(existing)}, indent=2))
PYEOF
    ;;

  search)
    python3 << 'PYEOF'
import json, os, re

data_file = os.environ.get("DATA_FILE")
raw_args = os.environ.get("ARGS", "")

params = {}
tokens = raw_args.split()
i = 0
while i < len(tokens):
    if tokens[i].startswith("--") and i + 1 < len(tokens):
        params[tokens[i][2:]] = tokens[i + 1]
        i += 2
    else:
        i += 1

query = params.get("query", "")
field = params.get("field", "both")

if not query:
    print(json.dumps({"error": "Please provide --query"}, indent=2))
    exit(1)

results = []
try:
    pattern = re.compile(query, re.IGNORECASE)
except:
    pattern = None

with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        key = rec.get("key", "")
        value = str(rec.get("value", ""))

        match = False
        if field in ("key", "both"):
            if pattern:
                match = match or bool(pattern.search(key))
            else:
                match = match or query.lower() in key.lower()
        if field in ("value", "both"):
            if pattern:
                match = match or bool(pattern.search(value))
            else:
                match = match or query.lower() in value.lower()

        if match:
            results.append({
                "key": key,
                "value": rec.get("value"),
                "tags": rec.get("tags", []),
                "created_at": rec.get("created_at")
            })

print(json.dumps({"query": query, "field": field, "count": len(results), "results": results}, indent=2))
PYEOF
    ;;

  config)
    python3 << 'PYEOF'
import json, os

config_file = os.environ.get("CONFIG_FILE")
raw_args = os.environ.get("ARGS", "")

with open(config_file, "r") as f:
    config = json.load(f)

if "--set" in raw_args:
    tokens = raw_args.split()
    for i, t in enumerate(tokens):
        if t == "--set" and i + 1 < len(tokens):
            kv = tokens[i + 1]
            if "=" in kv:
                k, v = kv.split("=", 1)
                try:
                    v = int(v)
                except:
                    pass
                config[k] = v

    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    print(json.dumps({"status": "updated", "config": config}, indent=2))
else:
    print(json.dumps(config, indent=2))
PYEOF
    ;;

  help)
    show_help
    ;;

  version)
    echo "{\"tool\": \"cache\", \"version\": \"$VERSION\"}"
    ;;

  *)
    echo "{\"error\": \"Unknown command: $COMMAND. Run 'help' for usage.\"}"
    exit 1
    ;;
esac
