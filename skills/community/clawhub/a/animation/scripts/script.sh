#!/usr/bin/env bash
# animation/scripts/script.sh — CSS/SVG Animation Code Generator
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail

VERSION="1.0.0"
DATA_DIR="$HOME/.animation"
DATA_FILE="$DATA_DIR/data.jsonl"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

COMMAND="${1:-help}"
shift 2>/dev/null || true

show_help() {
  cat << 'EOF'
Animation — CSS/SVG Animation Code Generator v1.0.0

Usage: bash script.sh <command> [options]

Commands:
  create      Create a new CSS or SVG animation
  keyframe    Generate a @keyframes block
  transition  Generate a CSS transition snippet
  timing      Show or set timing-function
  easing      List easing curves or define custom
  sequence    Build a multi-step animation sequence
  loop        Set loop/iteration count
  chain       Chain animations with delays
  export      Export animations to CSS/SVG file
  preview     Generate HTML preview page
  list        List all stored animations
  help        Show this help message
  version     Print version

Options (vary by command):
  --name        Animation name
  --type        css or svg (default: css)
  --property    CSS property to animate
  --from        Start value
  --to          End value
  --duration    Duration (e.g., 0.5s, 500ms)
  --easing      Easing function
  --steps       Keyframe steps (format: 'pct:value;pct:value')
  --names       Comma-separated animation names
  --delay       Delay between chained animations
  --count       Loop count (number or 'infinite')
  --mode        Sequence mode (sequential or parallel)
  --format      Export format (css or svg)
  --output      Output file path
  --id          Animation ID
EOF
}

case "$COMMAND" in
  create)
    python3 << 'PYEOF'
import json, os, sys, uuid, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
args = sys.argv[1:] if len(sys.argv) > 1 else []

# Parse arguments from parent env
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

name = params.get("name", "untitled")
anim_type = params.get("type", "css")
prop = params.get("property", "opacity")
from_val = params.get("from", "0")
to_val = params.get("to", "1")
duration = params.get("duration", "0.5s")
easing = params.get("easing", "ease")

anim_id = str(uuid.uuid4())[:8]
now = datetime.datetime.utcnow().isoformat() + "Z"

if anim_type == "css":
    code = f"""@keyframes {name} {{
  from {{ {prop}: {from_val}; }}
  to {{ {prop}: {to_val}; }}
}}

.{name} {{
  animation: {name} {duration} {easing};
}}"""
else:
    code = f"""<svg xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" fill="blue">
    <animate attributeName="{prop}"
             from="{from_val}" to="{to_val}"
             dur="{duration}" fill="freeze"/>
  </rect>
</svg>"""

record = {
    "id": anim_id,
    "name": name,
    "type": anim_type,
    "property": prop,
    "from": from_val,
    "to": to_val,
    "duration": duration,
    "easing": easing,
    "code": code,
    "loop_count": 1,
    "created_at": now
}

with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(json.dumps({"status": "created", "id": anim_id, "name": name, "code": code}, indent=2))
PYEOF
    ;;

  keyframe)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os, sys, uuid, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

name = params.get("name", "anim")
steps_raw = params.get("steps", "0%:initial;100%:final")

lines = []
for step in steps_raw.split(";"):
    parts = step.split(":", 1)
    if len(parts) == 2:
        lines.append(f"  {parts[0].strip()} {{ transform: {parts[1].strip()}; }}")

code = f"@keyframes {name} {{\n" + "\n".join(lines) + "\n}"

anim_id = str(uuid.uuid4())[:8]
now = datetime.datetime.utcnow().isoformat() + "Z"

record = {
    "id": anim_id,
    "name": name,
    "type": "keyframe",
    "code": code,
    "steps": steps_raw,
    "loop_count": 1,
    "created_at": now
}

with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(json.dumps({"status": "created", "id": anim_id, "name": name, "code": code}, indent=2))
PYEOF
    ;;

  transition)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os, sys, uuid, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

prop = params.get("property", "all")
duration = params.get("duration", "0.3s")
easing = params.get("easing", "ease")
delay = params.get("delay", "0s")

code = f"transition: {prop} {duration} {easing} {delay};"
name = params.get("name", f"transition-{prop}")

anim_id = str(uuid.uuid4())[:8]
now = datetime.datetime.utcnow().isoformat() + "Z"

record = {
    "id": anim_id,
    "name": name,
    "type": "transition",
    "property": prop,
    "duration": duration,
    "easing": easing,
    "delay": delay,
    "code": code,
    "created_at": now
}

with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(json.dumps({"status": "created", "id": anim_id, "name": name, "code": code}, indent=2))
PYEOF
    ;;

  timing)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

name = params.get("name", "")
new_timing = params.get("set", "")

if not name:
    print(json.dumps({"error": "Please provide --name"}, indent=2))
    exit(1)

records = []
found = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("name") == name:
            found = True
            if new_timing:
                rec["easing"] = new_timing
                old_code = rec.get("code", "")
                rec["code"] = old_code  # simplified; real impl would rewrite
                print(json.dumps({"status": "updated", "name": name, "timing": new_timing}, indent=2))
            else:
                print(json.dumps({"name": name, "timing": rec.get("easing", "ease")}, indent=2))
        records.append(rec)

if not found:
    print(json.dumps({"error": f"Animation '{name}' not found"}, indent=2))
    exit(1)

if new_timing:
    with open(data_file, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
PYEOF
    ;;

  easing)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os

raw_args = os.environ.get("ARGS", "")
easings = {
    "ease": "cubic-bezier(0.25, 0.1, 0.25, 1.0)",
    "ease-in": "cubic-bezier(0.42, 0, 1.0, 1.0)",
    "ease-out": "cubic-bezier(0, 0, 0.58, 1.0)",
    "ease-in-out": "cubic-bezier(0.42, 0, 0.58, 1.0)",
    "linear": "cubic-bezier(0, 0, 1, 1)",
    "ease-in-back": "cubic-bezier(0.36, 0, 0.66, -0.56)",
    "ease-out-back": "cubic-bezier(0.34, 1.56, 0.64, 1)",
    "ease-in-out-back": "cubic-bezier(0.68, -0.6, 0.32, 1.6)",
    "ease-in-circ": "cubic-bezier(0.55, 0, 1, 0.45)",
    "ease-out-circ": "cubic-bezier(0, 0.55, 0.45, 1)",
    "ease-in-quad": "cubic-bezier(0.11, 0, 0.5, 0)",
    "ease-out-quad": "cubic-bezier(0.5, 1, 0.89, 1)",
    "bounce": "cubic-bezier(0.34, 1.56, 0.64, 1)"
}

if "--list" in raw_args:
    result = [{"name": k, "value": v} for k, v in easings.items()]
    print(json.dumps(result, indent=2))
else:
    params = {}
    tokens = raw_args.split()
    i = 0
    while i < len(tokens):
        if tokens[i].startswith("--") and i + 1 < len(tokens):
            params[tokens[i][2:]] = tokens[i + 1]
            i += 2
        else:
            i += 1
    name = params.get("name", "")
    if name in easings:
        print(json.dumps({"name": name, "value": easings[name]}, indent=2))
    elif name:
        print(json.dumps({"name": name, "value": name, "note": "custom value"}, indent=2))
    else:
        result = [{"name": k, "value": v} for k, v in easings.items()]
        print(json.dumps(result, indent=2))
PYEOF
    ;;

  sequence)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os, uuid, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

names_str = params.get("names", "")
mode = params.get("mode", "sequential")

if not names_str:
    print(json.dumps({"error": "Please provide --names (comma-separated)"}, indent=2))
    exit(1)

names = [n.strip() for n in names_str.split(",")]

animations = {}
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("name") in names:
            animations[rec["name"]] = rec

found = [n for n in names if n in animations]
missing = [n for n in names if n not in animations]

if mode == "sequential":
    delay_acc = 0.0
    parts = []
    for n in found:
        dur = animations[n].get("duration", "1s")
        dur_val = float(dur.replace("s", "").replace("ms", "")) if "ms" not in dur else float(dur.replace("ms", "")) / 1000
        parts.append(f"  /* {n}: starts at {delay_acc}s */\n  animation: {n} {dur} ease {delay_acc}s;")
        delay_acc += dur_val
    code = "/* Sequential Sequence */\n" + "\n".join(parts)
else:
    parts = [f"  {n} {animations[n].get('duration', '1s')} ease" for n in found]
    code = "/* Parallel Sequence */\nanimation: " + ",\n           ".join(parts) + ";"

seq_id = str(uuid.uuid4())[:8]
now = datetime.datetime.utcnow().isoformat() + "Z"

record = {
    "id": seq_id,
    "name": f"sequence-{seq_id}",
    "type": "sequence",
    "mode": mode,
    "animations": found,
    "code": code,
    "created_at": now
}

with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

result = {"status": "created", "id": seq_id, "mode": mode, "animations": found, "code": code}
if missing:
    result["missing"] = missing
print(json.dumps(result, indent=2))
PYEOF
    ;;

  loop)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

name = params.get("name", "")
count = params.get("count", "")

if not name:
    print(json.dumps({"error": "Please provide --name"}, indent=2))
    exit(1)

records = []
found = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("name") == name:
            found = True
            if count:
                rec["loop_count"] = count
                code = rec.get("code", "")
                iteration = "infinite" if count == "infinite" else count
                rec["code"] = code + f"\n/* animation-iteration-count: {iteration}; */"
                print(json.dumps({"status": "updated", "name": name, "loop_count": count}, indent=2))
            else:
                print(json.dumps({"name": name, "loop_count": rec.get("loop_count", 1)}, indent=2))
        records.append(rec)

if not found:
    print(json.dumps({"error": f"Animation '{name}' not found"}, indent=2))
    exit(1)

if count:
    with open(data_file, "w") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
PYEOF
    ;;

  chain)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os, uuid, datetime

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

names_str = params.get("names", "")
delay = params.get("delay", "0.2s")

if not names_str:
    print(json.dumps({"error": "Please provide --names (comma-separated)"}, indent=2))
    exit(1)

names = [n.strip() for n in names_str.split(",")]
delay_val = float(delay.replace("s", "").replace("ms", "")) if "ms" not in delay else float(delay.replace("ms", "")) / 1000

animations = {}
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("name") in names:
            animations[rec["name"]] = rec

parts = []
acc = 0.0
for n in names:
    if n in animations:
        dur = animations[n].get("duration", "1s")
        parts.append(f"  /* {n}: delay {acc}s */\n  animation: {n} {dur} ease {acc}s forwards;")
        dur_val = float(dur.replace("s", "").replace("ms", "")) if "ms" not in dur else float(dur.replace("ms", "")) / 1000
        acc += dur_val + delay_val

code = "/* Chained Animations */\n" + "\n\n".join(parts)

chain_id = str(uuid.uuid4())[:8]
now = datetime.datetime.utcnow().isoformat() + "Z"

record = {
    "id": chain_id,
    "name": f"chain-{chain_id}",
    "type": "chain",
    "animations": names,
    "delay": delay,
    "code": code,
    "created_at": now
}

with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(json.dumps({"status": "created", "id": chain_id, "animations": names, "delay": delay, "code": code}, indent=2))
PYEOF
    ;;

  export)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

name = params.get("name", "")
fmt = params.get("format", "css")
output = params.get("output", "")

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if not name or rec.get("name") == name:
            records.append(rec)

if not records:
    print(json.dumps({"error": "No animations found"}, indent=2))
    exit(1)

if fmt == "css":
    content = "/* Generated by Animation Skill v1.0.0 */\n\n"
    content += "\n\n".join(rec.get("code", "") for rec in records)
elif fmt == "svg":
    content = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg">\n'
    for rec in records:
        if rec.get("type") == "svg":
            content += rec.get("code", "") + "\n"
        else:
            content += f'  <!-- CSS animation: {rec.get("name", "unknown")} -->\n'
    content += "</svg>"
else:
    content = json.dumps(records, indent=2)

if output:
    with open(output, "w") as f:
        f.write(content)
    print(json.dumps({"status": "exported", "file": output, "count": len(records)}, indent=2))
else:
    print(content)
PYEOF
    ;;

  preview)
    export ARGS="$*"
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))
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

name = params.get("name", "")
output = params.get("output", "preview.html")

animations = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if not name or rec.get("name") == name:
            animations.append(rec)

css_code = "\n".join(rec.get("code", "") for rec in animations if rec.get("type") in ("css", "keyframe", "transition"))

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Animation Preview</title>
  <style>
    body {{ font-family: sans-serif; padding: 40px; background: #1a1a2e; color: #eee; }}
    .preview-box {{
      width: 120px; height: 120px; background: #e94560;
      margin: 30px auto; border-radius: 12px;
    }}
    {css_code}
  </style>
</head>
<body>
  <h1>Animation Preview</h1>
  <p>Animations: {', '.join(r.get('name', '?') for r in animations)}</p>
  <div class="preview-box {' '.join(r.get('name', '') for r in animations)}"></div>
</body>
</html>"""

with open(output, "w") as f:
    f.write(html)

print(json.dumps({"status": "preview_generated", "file": output, "animations": len(animations)}, indent=2))
PYEOF
    ;;

  list)
    python3 << 'PYEOF'
import json, os

data_file = os.environ.get("DATA_FILE", os.path.expanduser("~/.animation/data.jsonl"))

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        records.append({
            "id": rec.get("id"),
            "name": rec.get("name"),
            "type": rec.get("type"),
            "duration": rec.get("duration", ""),
            "created_at": rec.get("created_at")
        })

if records:
    print(json.dumps(records, indent=2))
else:
    print(json.dumps({"message": "No animations stored yet"}, indent=2))
PYEOF
    ;;

  help)
    show_help
    ;;

  version)
    echo "{\"tool\": \"animation\", \"version\": \"$VERSION\"}"
    ;;

  *)
    echo "{\"error\": \"Unknown command: $COMMAND. Run 'help' for usage.\"}"
    exit 1
    ;;
esac
