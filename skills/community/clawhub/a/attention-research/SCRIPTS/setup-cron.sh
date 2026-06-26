#!/bin/bash
#
# attention-research: Setup Cron
# Reads topics.yaml and registers cron jobs in ~/.openclaw/cron/jobs.json

set -euo pipefail

SKILL_ROOT="${ATTENTION_RESEARCH_ROOT:-$HOME/.openclaw/skills/attention-research}"
CONFIG_DIR="$SKILL_ROOT/CONFIG"
CRON_JOBS_FILE="$HOME/.openclaw/cron/jobs.json"

ensure_cron_file() {
  mkdir -p "$(dirname "$CRON_JOBS_FILE")"
  if [[ ! -f "$CRON_JOBS_FILE" ]]; then
    echo '{"version": 1, "jobs": []}' > "$CRON_JOBS_FILE"
  fi
  python3 -c "import json; d=json.load(open('$CRON_JOBS_FILE')); assert 'jobs' in d" 2>/dev/null || {
    echo "ERROR: cron jobs file invalid"; exit 1; }
}

job_exists() {
  python3 -c "
import json
d = json.load(open('$CRON_JOBS_FILE'))
for j in d.get('jobs', []):
    if j.get('name') == '$1': exit(0)
exit(1)
" 2>/dev/null
}

register_job() {
  local name="$1" cron_expr="$2" script="$3"
  job_exists "$name" && { echo "SKIP: $name already registered"; return; }
  local job_json
  job_json=$(python3 -c "
import json
job = {'name': '$name', 'schedule': {'kind': 'cron', 'expression': '$cron_expr'},
       'script': '$script', 'enabled': True,
       'state': {'nextRunAtMs': None, 'lastRunStatus': None, 'lastRunAtMs': None}}
print(json.dumps(job))
")
  python3 - <<PY
import json
d = json.load(open('$CRON_JOBS_FILE'))
d['jobs'].append(json.loads('$job_json'))
json.dump(d, open('$CRON_JOBS_FILE', 'w'), indent=2)
PY
  echo "Registered: $name ($cron_expr)"
}

main() {
  echo "=== setup-cron ==="
  ensure_cron_file
  register_job "AR morning digest" "0 8 * * *" "$SKILL_ROOT/SCRIPTS/research-executor.sh --slot morning"
  register_job "AR afternoon thread update" "0 16 * * *" "$SKILL_ROOT/SCRIPTS/research-executor.sh --slot afternoon"
  echo "=== Done ==="
}

main