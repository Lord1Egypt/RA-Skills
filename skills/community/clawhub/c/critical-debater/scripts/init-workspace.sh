#!/bin/bash
# init-workspace.sh — Create debate workspace directory structure
set -euo pipefail

WORKSPACE_DIR="${1:?Usage: $0 <workspace_dir> <topic> <rounds>}"
TOPIC="${2:?Usage: $0 <workspace_dir> <topic> <rounds>}"
ROUNDS="${3:-3}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

mkdir -p "$WORKSPACE_DIR"/{evidence,claims,rounds,reports,logs}

for i in $(seq 1 "$ROUNDS"); do
  mkdir -p "$WORKSPACE_DIR/rounds/round_$i"
done

cat > "$WORKSPACE_DIR/config.json" <<EOF
{
  "topic": $(printf '%s' "$TOPIC" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),
  "round_count": $ROUNDS,
  "current_round": 0,
  "status": "initialized",
  "created_at": "$TIMESTAMP",
  "updated_at": "$TIMESTAMP"
}
EOF

echo '[]' > "$WORKSPACE_DIR/evidence/evidence_store.json"
echo '[]' > "$WORKSPACE_DIR/claims/claim_ledger.json"
touch "$WORKSPACE_DIR/logs/audit_trail.jsonl"

AUDIT_LINE=$(cat <<EOF
{"timestamp":"$TIMESTAMP","action":"workspace_initialized","topic":$(printf '%s' "$TOPIC" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'),"rounds":$ROUNDS}
EOF
)
echo "$AUDIT_LINE" >> "$WORKSPACE_DIR/logs/audit_trail.jsonl"

echo "Workspace initialized at $WORKSPACE_DIR"
