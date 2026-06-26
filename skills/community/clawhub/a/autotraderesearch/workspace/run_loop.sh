#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$SCRIPT_DIR"
AGENT_DIR="$WORKSPACE_DIR/agent"
PYTHON_BIN="${PYTHON:-python}"
AGENT="${AGENT:-codex}"
ROUNDS="${ROUNDS:-1}"
MODEL="${MODEL:-}"
CODEX_BIN="${CODEX_BIN:-codex}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

mkdir -p "$WORKSPACE_DIR/results" "$WORKSPACE_DIR/reports" "$WORKSPACE_DIR/data"

build_readonly_manifest() {
  local output_path="$1"

  "$PYTHON_BIN" - "$WORKSPACE_DIR" "$AGENT_DIR" "$output_path" <<'PY'
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

workspace = Path(sys.argv[1]).resolve()
agent_dir = Path(sys.argv[2]).resolve()
output_path = Path(sys.argv[3]).resolve()

entries = []
for path in sorted(workspace.rglob("*")):
    resolved = path.resolve()
    if resolved == agent_dir or agent_dir in resolved.parents:
        continue
    if path.is_symlink():
        rel = path.relative_to(workspace).as_posix()
        entries.append(f"{rel}\tSYMLINK\t{os.readlink(path)}")
        continue
    if not path.is_file():
        continue
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    rel = path.relative_to(workspace).as_posix()
    entries.append(f"{rel}\tFILE\t{digest}")

output_path.write_text("\n".join(entries), encoding="utf-8")
PY
}

check_readonly_drift() {
  local before_path="$1"
  local after_path="$2"

  "$PYTHON_BIN" - "$before_path" "$after_path" <<'PY'
from __future__ import annotations

import sys
from pathlib import Path

before_path = Path(sys.argv[1])
after_path = Path(sys.argv[2])

def load_manifest(path: Path) -> dict[str, str]:
    data = {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return data
    for line in text.splitlines():
        key, entry_type, value = line.split("\t", 2)
        data[key] = f"{entry_type}\t{value}"
    return data

before = load_manifest(before_path)
after = load_manifest(after_path)
drift = [path for path in sorted(set(before) | set(after)) if before.get(path) != after.get(path)]

if drift:
    print("Read-only files changed outside workspace/agent/:", file=sys.stderr)
    for path in drift:
        print(f"  - {path}", file=sys.stderr)
    raise SystemExit(1)
PY
}

run_codex() {
  local prompt="$1"
  local args=(
    exec
    --cd "$AGENT_DIR"
    --sandbox workspace-write
    --ask-for-approval never
  )

  if [ -n "$MODEL" ]; then
    args+=(--model "$MODEL")
  fi

  "$CODEX_BIN" "${args[@]}" "$prompt"
}

run_claude() {
  local prompt="$1"
  local args=(
    --print
    --permission-mode dontAsk
    --add-dir "$WORKSPACE_DIR"
    --allowedTools "Read,Edit,Bash"
  )

  if [ -n "$MODEL" ]; then
    args+=(--model "$MODEL")
  fi

  (
    cd "$AGENT_DIR"
    "$CLAUDE_BIN" "${args[@]}" "$prompt"
  )
}

run_iteration() {
  local iteration="$1"
  local before_manifest
  local after_manifest
  before_manifest="$(mktemp)"
  after_manifest="$(mktemp)"

  build_readonly_manifest "$before_manifest"

  local prompt
  prompt=$(cat <<EOF
AutoTradeResearch optimization iteration ${iteration} of ${ROUNDS}.

Work only inside the current agent directory.
Read ../AGENTS.md first, then read program.md.
Read ../reports/leaderboard.md if it exists.
Read ../results/results.tsv if it exists.
Choose either breadth or depth for this iteration.
Update strategy.py and program.md only if needed.
Write a simple backtesting.py-compatible AutoTradeStrategy.
Do not edit anything outside this directory.
Before finishing, review the strategy for obvious lookahead and backtesting.py compatibility issues.
EOF
)

  case "$AGENT" in
    codex)
      run_codex "$prompt"
      ;;
    claude)
      run_claude "$prompt"
      ;;
    *)
      echo "Unsupported AGENT value: $AGENT" >&2
      rm -f "$before_manifest" "$after_manifest"
      return 1
      ;;
  esac

  build_readonly_manifest "$after_manifest"
  check_readonly_drift "$before_manifest" "$after_manifest"

  (
    cd "$WORKSPACE_DIR"
    "$PYTHON_BIN" run_backtest.py
  )

  rm -f "$before_manifest" "$after_manifest"
}

for iteration in $(seq 1 "$ROUNDS"); do
  echo "== AutoTradeResearch iteration $iteration / $ROUNDS =="
  run_iteration "$iteration"
done
