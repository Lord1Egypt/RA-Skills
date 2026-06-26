#!/bin/bash
# scan-obsidian.sh - Scan Obsidian notes, auto-spawn ready tasks

source "$(dirname "$0")/config.sh"

SCAN_LOG="${LOGS_DIR}/scan-obsidian.log"
log() { echo "[$(date '+%H:%M:%S')] $1" >> "$SCAN_LOG"; }

log "=== Obsidian scan ==="

if [ -z "$SWARM_OBSIDIAN_DIR" ] || [ ! -d "$SWARM_OBSIDIAN_DIR" ]; then
    log "Obsidian dir not found or not configured"
    exit 0
fi

find "$SWARM_OBSIDIAN_DIR" -name "*.md" -not -name "_template.md" | while read -r NOTE_FILE; do
    PROJECT=$(basename "$NOTE_FILE" .md)
    log "Scanning: $PROJECT"

    MODIFIED_RECENTLY=$(find "$NOTE_FILE" -mmin -1 2>/dev/null | wc -l | tr -d ' ')
    if [ "$MODIFIED_RECENTLY" -gt 0 ]; then
        log "Skipping $PROJECT: debounce (modified <1min ago)"
        continue
    fi

    FILE_STATUS=$(grep -m1 '^status:' "$NOTE_FILE" 2>/dev/null | awk '{print $2}' | tr -d '"' || echo "active")
    if [ "$FILE_STATUS" = "stop" ]; then
        log "  status=stop, skipping"
        continue
    fi

    python3 << PYEOF >> "$SCAN_LOG" 2>&1
import os, re, subprocess, hashlib

note_file = r'''$NOTE_FILE'''
project = r'''$PROJECT'''
scripts_dir = r'''$SCRIPTS_DIR'''
logs_dir = r'''$LOGS_DIR'''

content = open(note_file, 'r', encoding='utf-8').read()

parts = re.split(r'(?m)^###\s+', content)
if len(parts) <= 1:
    raise SystemExit(0)

for part in parts[1:]:
    lines = part.splitlines()
    if not lines:
        continue

    task_name = lines[0].strip()
    block = "\n".join(lines[1:])

    m_status = re.search(r'(?m)^status:\s*(\S+)\s*$', block)
    if not m_status:
        continue
    status = m_status.group(1).strip().lower()
    if status != 'ready':
        continue

    desc_lines = re.findall(r'(?m)^>\s*(.+)$', block)
    if not desc_lines:
        print(f"  Skip task (no description): {task_name}")
        continue
    task_desc = "\n".join(line.strip() for line in desc_lines)

    if task_name.upper() == 'INIT_PROJECT':
        print(f"  Initializing project: {project}")
        result = subprocess.run([os.path.join(scripts_dir, 'new-project.sh'), project, note_file], capture_output=True, text=True)
        if result.returncode == 0:
            updated = content.replace(f"### {task_name}\nstatus: ready", f"### {task_name}\nstatus: done", 1)
            if updated != content:
                open(note_file, 'w', encoding='utf-8').write(updated)
                content = updated
                print("  ✓ INIT_PROJECT done")
        else:
            print(f"  ✗ INIT_PROJECT failed: {result.stderr}")
        continue

    normalized_desc = " ".join(task_desc.split())
    dedup_src = f"{project}\n{task_name}\n{normalized_desc}"
    dedup_key = hashlib.sha1(dedup_src.encode('utf-8')).hexdigest()[:12]
    dedup_flag = os.path.join(logs_dir, f".spawned-{dedup_key}")

    if os.path.exists(dedup_flag):
        print(f"  Already spawned: {task_name}")
        continue

    print(f"  Spawning task: {task_name}")
    result = subprocess.run([
        os.path.join(scripts_dir, 'spawn-agent.sh'),
        project, task_desc, '', 'normal', task_name, note_file, dedup_key
    ], capture_output=True, text=True)
    if result.returncode == 0:
        open(dedup_flag, 'w').close()
        print(f"  ✓ Spawned: {task_name}")
        updated = content.replace(f"### {task_name}\nstatus: ready", f"### {task_name}\nstatus: in_progress", 1)
        if updated != content:
            open(note_file, 'w', encoding='utf-8').write(updated)
            content = updated
    else:
        print(f"  ✗ Failed: {result.stderr}")
PYEOF

done

log "=== Scan complete ==="
