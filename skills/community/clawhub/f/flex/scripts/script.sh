#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# flex — CSS Flexbox Layout Generator
# Version: 1.0.0
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
###############################################################################

DATA_DIR="$HOME/.flex"
DATA_FILE="$DATA_DIR/data.jsonl"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

COMMAND="${1:-help}"
shift 2>/dev/null || true

case "$COMMAND" in

create)
  NAME="" DIRECTION="row" ITEMS="3"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name) NAME="$2"; shift 2;;
      --direction) DIRECTION="$2"; shift 2;;
      --items) ITEMS="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_NAME="$NAME"
  export FLEX_DIRECTION="$DIRECTION"
  export FLEX_ITEMS="$ITEMS"
  python3 << 'PYEOF'
import json, os, uuid, time

data_file = os.environ["FLEX_DATA_FILE"]
name = os.environ["FLEX_NAME"]
direction = os.environ["FLEX_DIRECTION"]
items = int(os.environ["FLEX_ITEMS"])

layout = {
    "id": str(uuid.uuid4())[:8],
    "name": name,
    "display": "flex",
    "flex_direction": direction,
    "flex_wrap": "nowrap",
    "justify_content": "flex-start",
    "align_items": "stretch",
    "gap": "0",
    "row_gap": None,
    "column_gap": None,
    "items": [{"index": i+1, "flex_grow": 0, "flex_shrink": 1, "flex_basis": "auto", "order": 0} for i in range(items)],
    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
}

with open(data_file, "a") as f:
    f.write(json.dumps(layout) + "\n")

print(f"✅ Layout created: {layout['id']}")
print(f"   Name: {name}")
print(f"   Direction: {direction}")
print(f"   Items: {items}")
print(f"   Class: .{name.replace(' ', '-').lower()}")
PYEOF
  ;;

row)
  NAME="" ITEMS="3" GAP="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name) NAME="$2"; shift 2;;
      --items) ITEMS="$2"; shift 2;;
      --gap) GAP="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_NAME="$NAME"
  export FLEX_ITEMS="$ITEMS"
  export FLEX_GAP="$GAP"
  python3 << 'PYEOF'
import json, os, uuid, time

data_file = os.environ["FLEX_DATA_FILE"]
name = os.environ["FLEX_NAME"]
items = int(os.environ["FLEX_ITEMS"])
gap = os.environ["FLEX_GAP"]

layout = {
    "id": str(uuid.uuid4())[:8],
    "name": name,
    "display": "flex",
    "flex_direction": "row",
    "flex_wrap": "nowrap",
    "justify_content": "flex-start",
    "align_items": "stretch",
    "gap": f"{gap}px" if gap != "0" else "0",
    "row_gap": None,
    "column_gap": None,
    "items": [{"index": i+1, "flex_grow": 0, "flex_shrink": 1, "flex_basis": "auto", "order": 0} for i in range(items)],
    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
}

with open(data_file, "a") as f:
    f.write(json.dumps(layout) + "\n")

print(f"✅ Row layout created: {layout['id']}")
print(f"   Name: {name}")
print(f"   Items: {items}, Gap: {layout['gap']}")
PYEOF
  ;;

column)
  NAME="" ITEMS="3" GAP="0"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name) NAME="$2"; shift 2;;
      --items) ITEMS="$2"; shift 2;;
      --gap) GAP="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_NAME="$NAME"
  export FLEX_ITEMS="$ITEMS"
  export FLEX_GAP="$GAP"
  python3 << 'PYEOF'
import json, os, uuid, time

data_file = os.environ["FLEX_DATA_FILE"]
name = os.environ["FLEX_NAME"]
items = int(os.environ["FLEX_ITEMS"])
gap = os.environ["FLEX_GAP"]

layout = {
    "id": str(uuid.uuid4())[:8],
    "name": name,
    "display": "flex",
    "flex_direction": "column",
    "flex_wrap": "nowrap",
    "justify_content": "flex-start",
    "align_items": "stretch",
    "gap": f"{gap}px" if gap != "0" else "0",
    "row_gap": None,
    "column_gap": None,
    "items": [{"index": i+1, "flex_grow": 0, "flex_shrink": 1, "flex_basis": "auto", "order": 0} for i in range(items)],
    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
}

with open(data_file, "a") as f:
    f.write(json.dumps(layout) + "\n")

print(f"✅ Column layout created: {layout['id']}")
print(f"   Name: {name}")
print(f"   Items: {items}, Gap: {layout['gap']}")
PYEOF
  ;;

wrap)
  ID="" VALUE="wrap"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --value) VALUE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$ID" ]]; then
    echo "Error: --id is required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_VALUE="$VALUE"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ["FLEX_ID"]
value = os.environ["FLEX_VALUE"]

entries = []
found = False
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            e = json.loads(line)
            if e.get("id") == target_id:
                e["flex_wrap"] = value
                found = True
            entries.append(e)

if not found:
    print(f"❌ Layout not found: {target_id}")
    exit(1)

with open(data_file, "w") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

print(f"✅ Updated flex-wrap to '{value}' on layout {target_id}")
PYEOF
  ;;

align)
  ID="" VALUE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --value) VALUE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$ID" || -z "$VALUE" ]]; then
    echo "Error: --id and --value are required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_VALUE="$VALUE"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ["FLEX_ID"]
value = os.environ["FLEX_VALUE"]

valid = ["flex-start", "flex-end", "center", "stretch", "baseline"]
if value not in valid:
    print(f"❌ Invalid value: {value}. Must be one of: {', '.join(valid)}")
    exit(1)

entries = []
found = False
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            e = json.loads(line)
            if e.get("id") == target_id:
                e["align_items"] = value
                found = True
            entries.append(e)

if not found:
    print(f"❌ Layout not found: {target_id}")
    exit(1)

with open(data_file, "w") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

print(f"✅ Updated align-items to '{value}' on layout {target_id}")
PYEOF
  ;;

justify)
  ID="" VALUE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --value) VALUE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$ID" || -z "$VALUE" ]]; then
    echo "Error: --id and --value are required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_VALUE="$VALUE"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ["FLEX_ID"]
value = os.environ["FLEX_VALUE"]

valid = ["flex-start", "flex-end", "center", "space-between", "space-around", "space-evenly"]
if value not in valid:
    print(f"❌ Invalid value: {value}. Must be one of: {', '.join(valid)}")
    exit(1)

entries = []
found = False
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            e = json.loads(line)
            if e.get("id") == target_id:
                e["justify_content"] = value
                found = True
            entries.append(e)

if not found:
    print(f"❌ Layout not found: {target_id}")
    exit(1)

with open(data_file, "w") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

print(f"✅ Updated justify-content to '{value}' on layout {target_id}")
PYEOF
  ;;

gap)
  ID="" VALUE="" ROW_GAP="" COL_GAP=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --value) VALUE="$2"; shift 2;;
      --row) ROW_GAP="$2"; shift 2;;
      --column) COL_GAP="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$ID" ]]; then
    echo "Error: --id is required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_GAP_VALUE="$VALUE"
  export FLEX_ROW_GAP="$ROW_GAP"
  export FLEX_COL_GAP="$COL_GAP"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ["FLEX_ID"]
gap_val = os.environ.get("FLEX_GAP_VALUE", "")
row_gap = os.environ.get("FLEX_ROW_GAP", "")
col_gap = os.environ.get("FLEX_COL_GAP", "")

entries = []
found = False
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            e = json.loads(line)
            if e.get("id") == target_id:
                if gap_val:
                    e["gap"] = f"{gap_val}px"
                if row_gap:
                    e["row_gap"] = f"{row_gap}px"
                if col_gap:
                    e["column_gap"] = f"{col_gap}px"
                found = True
            entries.append(e)

if not found:
    print(f"❌ Layout not found: {target_id}")
    exit(1)

with open(data_file, "w") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

msg = []
if gap_val: msg.append(f"gap: {gap_val}px")
if row_gap: msg.append(f"row-gap: {row_gap}px")
if col_gap: msg.append(f"column-gap: {col_gap}px")
print(f"✅ Updated {', '.join(msg)} on layout {target_id}")
PYEOF
  ;;

order)
  ID="" ITEM="" VALUE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --item) ITEM="$2"; shift 2;;
      --value) VALUE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$ID" || -z "$ITEM" || -z "$VALUE" ]]; then
    echo "Error: --id, --item, and --value are required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_ITEM="$ITEM"
  export FLEX_VALUE="$VALUE"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ["FLEX_ID"]
item_idx = int(os.environ["FLEX_ITEM"])
value = int(os.environ["FLEX_VALUE"])

entries = []
found = False
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            e = json.loads(line)
            if e.get("id") == target_id:
                for item in e.get("items", []):
                    if item["index"] == item_idx:
                        item["order"] = value
                        found = True
            entries.append(e)

if not found:
    print(f"❌ Layout or item not found: {target_id}, item {item_idx}")
    exit(1)

with open(data_file, "w") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

print(f"✅ Set order={value} on item {item_idx} in layout {target_id}")
PYEOF
  ;;

grow)
  ID="" ITEM="" VALUE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --item) ITEM="$2"; shift 2;;
      --value) VALUE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$ID" || -z "$ITEM" || -z "$VALUE" ]]; then
    echo "Error: --id, --item, and --value are required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_ITEM="$ITEM"
  export FLEX_VALUE="$VALUE"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ["FLEX_ID"]
item_idx = int(os.environ["FLEX_ITEM"])
value = int(os.environ["FLEX_VALUE"])

entries = []
found = False
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            e = json.loads(line)
            if e.get("id") == target_id:
                for item in e.get("items", []):
                    if item["index"] == item_idx:
                        item["flex_grow"] = value
                        found = True
            entries.append(e)

if not found:
    print(f"❌ Layout or item not found: {target_id}, item {item_idx}")
    exit(1)

with open(data_file, "w") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

print(f"✅ Set flex-grow={value} on item {item_idx} in layout {target_id}")
PYEOF
  ;;

shrink)
  ID="" ITEM="" VALUE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --item) ITEM="$2"; shift 2;;
      --value) VALUE="$2"; shift 2;;
      *) shift;;
    esac
  done
  if [[ -z "$ID" || -z "$ITEM" || -z "$VALUE" ]]; then
    echo "Error: --id, --item, and --value are required"
    exit 1
  fi
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_ITEM="$ITEM"
  export FLEX_VALUE="$VALUE"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ["FLEX_ID"]
item_idx = int(os.environ["FLEX_ITEM"])
value = int(os.environ["FLEX_VALUE"])

entries = []
found = False
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            e = json.loads(line)
            if e.get("id") == target_id:
                for item in e.get("items", []):
                    if item["index"] == item_idx:
                        item["flex_shrink"] = value
                        found = True
            entries.append(e)

if not found:
    print(f"❌ Layout or item not found: {target_id}, item {item_idx}")
    exit(1)

with open(data_file, "w") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

print(f"✅ Set flex-shrink={value} on item {item_idx} in layout {target_id}")
PYEOF
  ;;

export)
  ID="" ALL="" OUTPUT=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) ID="$2"; shift 2;;
      --all) ALL="1"; shift;;
      --output) OUTPUT="$2"; shift 2;;
      *) shift;;
    esac
  done
  export FLEX_DATA_FILE="$DATA_FILE"
  export FLEX_ID="$ID"
  export FLEX_ALL="$ALL"
  export FLEX_OUTPUT="$OUTPUT"
  python3 << 'PYEOF'
import json, os

data_file = os.environ["FLEX_DATA_FILE"]
target_id = os.environ.get("FLEX_ID", "")
export_all = os.environ.get("FLEX_ALL", "") == "1"
output = os.environ.get("FLEX_OUTPUT", "")

entries = []
if os.path.exists(data_file):
    with open(data_file) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

if target_id:
    entries = [e for e in entries if e.get("id") == target_id]
elif not export_all:
    print("Error: --id or --all is required")
    exit(1)

if not entries:
    print("⚠️  No layouts to export.")
    exit(0)

css_parts = []
for layout in entries:
    class_name = layout["name"].replace(" ", "-").lower()
    css = f".{class_name} {{\n"
    css += f"  display: flex;\n"
    css += f"  flex-direction: {layout['flex_direction']};\n"
    css += f"  flex-wrap: {layout['flex_wrap']};\n"
    css += f"  justify-content: {layout['justify_content']};\n"
    css += f"  align-items: {layout['align_items']};\n"
    if layout.get("gap") and layout["gap"] != "0":
        css += f"  gap: {layout['gap']};\n"
    if layout.get("row_gap"):
        css += f"  row-gap: {layout['row_gap']};\n"
    if layout.get("column_gap"):
        css += f"  column-gap: {layout['column_gap']};\n"
    css += "}\n"

    for item in layout.get("items", []):
        has_custom = item.get("flex_grow", 0) != 0 or item.get("flex_shrink", 1) != 1 or item.get("order", 0) != 0 or item.get("flex_basis", "auto") != "auto"
        if has_custom:
            css += f"\n.{class_name} > *:nth-child({item['index']}) {{\n"
            if item.get("flex_grow", 0) != 0:
                css += f"  flex-grow: {item['flex_grow']};\n"
            if item.get("flex_shrink", 1) != 1:
                css += f"  flex-shrink: {item['flex_shrink']};\n"
            if item.get("flex_basis", "auto") != "auto":
                css += f"  flex-basis: {item['flex_basis']};\n"
            if item.get("order", 0) != 0:
                css += f"  order: {item['order']};\n"
            css += "}\n"

    css_parts.append(css)

result = "\n".join(css_parts)

if output:
    with open(output, "w") as f:
        f.write(result)
    print(f"✅ Exported {len(entries)} layout(s) to {output}")
else:
    print(result)
PYEOF
  ;;

help)
  cat << 'HELPEOF'
flex — CSS Flexbox Layout Generator v1.0.0

Commands:
  create      Create a new flex container layout
  row         Create a horizontal row layout
  column      Create a vertical column layout
  wrap        Set flex-wrap property
  align       Set align-items property
  justify     Set justify-content property
  gap         Set gap property
  order       Set item order
  grow        Set flex-grow for an item
  shrink      Set flex-shrink for an item
  export      Export layouts as CSS
  help        Show this help message
  version     Show version

Usage: bash scripts/script.sh <command> [options]

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
  ;;

version)
  echo "flex v1.0.0"
  ;;

*)
  echo "Unknown command: $COMMAND"
  echo "Run 'bash scripts/script.sh help' for usage."
  exit 1
  ;;

esac
