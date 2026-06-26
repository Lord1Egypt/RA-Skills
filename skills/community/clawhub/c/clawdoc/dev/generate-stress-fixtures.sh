#!/usr/bin/env bash
set -euo pipefail

# generate-stress-fixtures.sh
# Generates 50+ synthetic JSONL session files for stress-testing all 12 detectors.
# Each fixture has a known expected outcome (which patterns should/shouldn't fire).
# Output: tests/fixtures/stress/ directory with fixtures + manifest.tsv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/../tests/fixtures/stress"

if [ -d "$OUT_DIR" ] && [ "$(ls -A "$OUT_DIR" 2>/dev/null)" ]; then
  echo "Output directory '$OUT_DIR' exists and is not empty."
  printf "Remove it and regenerate? [y/N] "
  read -r CONFIRM
  if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Aborted." >&2
    exit 1
  fi
fi

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

MANIFEST="$OUT_DIR/manifest.tsv"
echo -e "fixture\tdescription\texpect_patterns\texpect_not_patterns" > "$MANIFEST"

# Counter
N=0

# Helper: generate session header
session_header() {
  local sid="$1" model="${2:-anthropic/claude-sonnet-4-6}" key="${3:-agent:main:main}"
  local ts="${4:-2026-03-13T10:00:00.000Z}"
  echo "{\"type\":\"session\",\"timestamp\":\"$ts\",\"sessionId\":\"$sid\",\"agentId\":\"main\",\"model\":\"$model\",\"sessionKey\":\"$key\"}"
}

# Helper: user message
user_msg() {
  local ts="$1" text="$2"
  echo "{\"type\":\"message\",\"timestamp\":\"$ts\",\"message\":{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"$text\"}]}}"
}

# Helper: assistant message with toolCall
assistant_tool() {
  local ts="$1" tool="$2" input_json="$3" in_tok="$4" out_tok="${5:-40}" cost="$6"
  echo "{\"type\":\"message\",\"timestamp\":\"$ts\",\"message\":{\"role\":\"assistant\",\"content\":[{\"type\":\"text\",\"text\":\"Working...\",\"citations\":[]},{\"type\":\"toolCall\",\"id\":\"tc_$(printf '%03d' "$RANDOM")\",\"name\":\"$tool\",\"input\":$input_json}],\"usage\":{\"inputTokens\":$in_tok,\"outputTokens\":$out_tok,\"contextTokens\":128000,\"cost\":{\"total\":$cost}}}}"
}

# Helper: assistant text-only message
assistant_text() {
  local ts="$1" text="$2" in_tok="$3" out_tok="${4:-40}" cost="$5"
  echo "{\"type\":\"message\",\"timestamp\":\"$ts\",\"message\":{\"role\":\"assistant\",\"content\":[{\"type\":\"text\",\"text\":\"$text\"}],\"usage\":{\"inputTokens\":$in_tok,\"outputTokens\":$out_tok,\"contextTokens\":128000,\"cost\":{\"total\":$cost}}}}"
}

# Helper: tool result
tool_result() {
  local ts="$1" text="$2"
  echo "{\"type\":\"message\",\"timestamp\":\"$ts\",\"message\":{\"role\":\"toolResult\",\"content\":[{\"type\":\"text\",\"text\":\"$text\"}]}}"
}

# Helper: increment timestamp by N seconds
ts_add() {
  # Just increment the seconds portion simplistically
  local base="$1" secs="$2"
  local min_part sec_part
  sec_part=$(echo "$base" | grep -oE ':[0-9]{2}\.' | head -1 | tr -d ':.')
  sec_part=$((10#$sec_part + secs))
  local new_min=$((sec_part / 60))
  local new_sec=$((sec_part % 60))
  # Simple: just use fixed format with incrementing minutes
  printf "2026-03-13T10:%02d:%02d.000Z" "$new_min" "$new_sec"
}

add_manifest() {
  local file="$1" desc="$2" expect="$3" not_expect="${4:-}"
  echo -e "$file\t$desc\t$expect\t$not_expect" >> "$MANIFEST"
}

# ============================================================================
# CATEGORY 1: Task Drift — Post-compaction directory divergence (pattern 12A)
# ============================================================================

# S01: Classic drift — API work → compaction → UI work
gen_drift_classic() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-classic.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Fix the login endpoint bug"
    for i in 1 2 3 4 5; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/api/auth/handler-$i.ts\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.003*$((i+2))" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export function handler$i() {}"
    done
    assistant_tool "$(ts_add x 180)" "write" "{\"path\":\"src/api/auth/handler-1.ts\"}" 15000 60 0.048
    tool_result "$(ts_add x 195)" "File written"
    # Compaction
    assistant_text "$(ts_add x 210)" "Compaction triggered." 80000 20 0.240
    assistant_text "$(ts_add x 225)" "Compaction complete." 28000 20 0.084
    # Drift: now touching UI
    for i in 1 2 3 4 5; do
      assistant_tool "$(ts_add x $((240+i*30)))" "read" "{\"path\":\"src/ui/pages/page-$i.tsx\"}" "$((30000+i*2000))" 40 "$(echo "scale=6;0.090+$i*0.006" | bc)"
      tool_result "$(ts_add x $((240+i*30+15)))" "export const Page$i = () => <div>page</div>"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Classic drift: API→compaction→UI" "12" ""
}

# S02: Drift to docs after compaction
gen_drift_docs() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-docs.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Optimize the database queries"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/db/query-$i.sql\"}" "$((4000+i*3000))" 40 "$(echo "scale=6;0.012+$i*0.009" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "SELECT * FROM table_$i"
    done
    assistant_tool "$(ts_add x 150)" "write" "{\"path\":\"src/db/query-1.sql\"}" 16000 60 0.048
    tool_result "$(ts_add x 165)" "File written"
    assistant_text "$(ts_add x 180)" "Compaction triggered." 85000 20 0.255
    assistant_text "$(ts_add x 195)" "Compaction complete." 30000 20 0.090
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((210+i*30)))" "read" "{\"path\":\"docs/guides/guide-$i.md\"}" "$((32000+i*2000))" 40 "$(echo "scale=6;0.096+$i*0.006" | bc)"
      tool_result "$(ts_add x $((210+i*30+15)))" "# Guide $i"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Drift: DB work→compaction→docs" "12" ""
}

# S03: Drift to tests directory (borderline — 3 new dir calls, exactly at threshold)
gen_drift_borderline() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-borderline.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Add validation to the form"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/components/form-$i.tsx\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export const Form$i = () => {}"
    done
    assistant_text "$(ts_add x 120)" "Compaction." 75000 20 0.225
    assistant_text "$(ts_add x 135)" "Done." 26000 20 0.078
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((150+i*30)))" "read" "{\"path\":\"tests/integration/test-$i.spec.ts\"}" "$((28000+i*2000))" 40 "$(echo "scale=6;0.084+$i*0.006" | bc)"
      tool_result "$(ts_add x $((150+i*30+15)))" "describe('test $i', () => {})"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Drift borderline: exactly 3 new-dir calls at threshold" "12" ""
}

# S04: No drift — same dirs before and after compaction
gen_no_drift_same_dirs() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-nodrift-same-dirs.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Refactor auth module"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/auth/module-$i.ts\"}" "$((5000+i*3000))" 40 "$(echo "scale=6;0.015+$i*0.009" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export function mod$i() {}"
    done
    assistant_text "$(ts_add x 150)" "Compaction." 78000 20 0.234
    assistant_text "$(ts_add x 165)" "Done." 27000 20 0.081
    for i in 5 6 7 8; do
      assistant_tool "$(ts_add x $((180+(i-4)*30)))" "read" "{\"path\":\"src/auth/module-$i.ts\"}" "$((29000+(i-4)*2000))" 40 "$(echo "scale=6;0.087+(($i-4))*0.006" | bc)"
      tool_result "$(ts_add x $((180+(i-4)*30+15)))" "export function mod$i() {}"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "No drift: same directory before/after compaction" "none" "12"
}

# S05: No drift — only 2 new-dir calls (below threshold)
gen_no_drift_below_threshold() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-nodrift-below-thresh.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Fix CSS bug"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/styles/main-$i.css\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" ".class-$i { color: red; }"
    done
    assistant_text "$(ts_add x 120)" "Compaction." 72000 20 0.216
    assistant_text "$(ts_add x 135)" "Done." 25000 20 0.075
    # Only 2 calls to new dir — below threshold
    for i in 1 2; do
      assistant_tool "$(ts_add x $((150+i*30)))" "read" "{\"path\":\"src/components/widget-$i.tsx\"}" "$((27000+i*2000))" 40 "$(echo "scale=6;0.081+$i*0.006" | bc)"
      tool_result "$(ts_add x $((150+i*30+15)))" "export const Widget$i = () => {}"
    done
    # Plus 2 calls to original dir
    for i in 4 5; do
      assistant_tool "$(ts_add x $((210+(i-3)*30)))" "read" "{\"path\":\"src/styles/main-$i.css\"}" "$((31000+(i-3)*2000))" 40 "$(echo "scale=6;0.093+(($i-3))*0.006" | bc)"
      tool_result "$(ts_add x $((210+(i-3)*30+15)))" ".class-$i { color: blue; }"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "No drift: only 2 new-dir calls (below threshold)" "none" "12"
}

# ============================================================================
# CATEGORY 2: Exploration spiral (pattern 12B)
# ============================================================================

# S06: 15 consecutive reads — clear spiral
gen_spiral_15() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-15-reads.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Update the payment form"
    for i in $(seq 1 15); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/payments/file-$i.ts\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.003+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "export const pay$i = {};"
    done
    assistant_tool "$(ts_add x 320)" "write" "{\"path\":\"src/payments/file-1.ts\"}" 12000 60 0.036
    tool_result "$(ts_add x 335)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Exploration spiral: 15 consecutive reads" "12" ""
}

# S07: Exactly 10 reads — at threshold
gen_spiral_10() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-10-reads.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Fix the router"
    for i in $(seq 1 10); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/router/route-$i.ts\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.003+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "export const route$i = {};"
    done
    assistant_tool "$(ts_add x 220)" "write" "{\"path\":\"src/router/route-1.ts\"}" 9000 60 0.027
    tool_result "$(ts_add x 235)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Exploration spiral: exactly 10 reads (at threshold)" "12" ""
}

# S08: 9 reads — below threshold
gen_spiral_9() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-9-reads.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Add logging"
    for i in $(seq 1 9); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/logger/log-$i.ts\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.003+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "export const log$i = {};"
    done
    assistant_tool "$(ts_add x 200)" "write" "{\"path\":\"src/logger/log-1.ts\"}" 8000 60 0.024
    tool_result "$(ts_add x 215)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "No spiral: 9 reads (below threshold)" "none" "12"
}

# S09: Mixed read + grep — still counts as exploration
gen_spiral_mixed() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-mixed-tools.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Find and fix the bug"
    for i in $(seq 1 6); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/core/file-$i.ts\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.003+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "export const fn$i = {};"
    done
    for i in $(seq 1 5); do
      assistant_tool "$(ts_add x $((140+i*20)))" "Grep" "{\"pattern\":\"TODO\",\"path\":\"src/\"}" "$((6000+i*500))" 40 "$(echo "scale=6;0.018+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((140+i*20+10)))" "src/core/file-$i.ts:42: // TODO: fix this"
    done
    assistant_tool "$(ts_add x 260)" "write" "{\"path\":\"src/core/file-1.ts\"}" 10000 60 0.030
    tool_result "$(ts_add x 275)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Exploration spiral: mixed read+Grep (11 total)" "12" ""
}

# S10: Reads broken by exec (not a spiral — exec breaks the run)
gen_spiral_broken_by_exec() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-broken-exec.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Debug test failures"
    for i in $(seq 1 5); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/test/spec-$i.ts\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.003+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "describe('spec $i', () => {})"
    done
    assistant_tool "$(ts_add x 120)" "exec" "{\"command\":\"npm test\"}" 6000 40 0.018
    tool_result "$(ts_add x 135)" "Tests: 5 passed"
    for i in $(seq 6 10); do
      assistant_tool "$(ts_add x $((150+(i-5)*20)))" "read" "{\"path\":\"src/test/spec-$i.ts\"}" "$((7000+(i-5)*500))" 40 "$(echo "scale=6;0.021+(($i-5))*0.0015" | bc)"
      tool_result "$(ts_add x $((150+(i-5)*20+10)))" "describe('spec $i', () => {})"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "No spiral: reads broken by exec in middle" "none" "12"
}

# S11: Reads broken by a write in the middle
gen_spiral_broken_by_write() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-broken-write.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Review and update config"
    for i in $(seq 1 5); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"config/setting-$i.yaml\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.003+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "setting_$i: true"
    done
    assistant_tool "$(ts_add x 120)" "write" "{\"path\":\"config/setting-1.yaml\"}" 6000 60 0.018
    tool_result "$(ts_add x 135)" "File written"
    for i in $(seq 6 10); do
      assistant_tool "$(ts_add x $((150+(i-5)*20)))" "read" "{\"path\":\"config/setting-$i.yaml\"}" "$((7000+(i-5)*500))" 40 "$(echo "scale=6;0.021+(($i-5))*0.0015" | bc)"
      tool_result "$(ts_add x $((150+(i-5)*20+10)))" "setting_$i: false"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "No spiral: reads broken by write in middle" "none" "12"
}

# S12: Glob-heavy exploration
gen_spiral_glob() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-glob-heavy.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Find all test files"
    for i in $(seq 1 12); do
      assistant_tool "$(ts_add x $((i*20)))" "Glob" "{\"pattern\":\"src/**/*-$i.test.ts\"}" "$((3000+i*400))" 40 "$(echo "scale=6;0.003+$i*0.0012" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "src/module-$i/index.test.ts"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Exploration spiral: 12 consecutive Glob calls" "12" ""
}

# ============================================================================
# CATEGORY 3: Healthy sessions — should NOT trigger pattern 12
# ============================================================================

# S13-S17: Various healthy patterns
gen_healthy_short() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-healthy-short.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "What time is it in Tokyo?"
    assistant_tool "$(ts_add x 30)" "search_web" "{\"query\":\"time in Tokyo\"}" 800 40 0.003
    tool_result "$(ts_add x 45)" "3:42 PM JST"
    assistant_text "$(ts_add x 60)" "It is 3:42 PM in Tokyo." 1100 30 0.004
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Healthy: short 1-tool session" "none" "12"
}

gen_healthy_read_write_balanced() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-healthy-balanced.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Rename the function"
    assistant_tool "$(ts_add x 30)" "read" "{\"path\":\"src/utils.ts\"}" 3000 40 0.009
    tool_result "$(ts_add x 45)" "export function oldName() {}"
    assistant_tool "$(ts_add x 60)" "write" "{\"path\":\"src/utils.ts\"}" 4000 60 0.012
    tool_result "$(ts_add x 75)" "File written"
    assistant_tool "$(ts_add x 90)" "read" "{\"path\":\"src/index.ts\"}" 5000 40 0.015
    tool_result "$(ts_add x 105)" "import { oldName } from './utils'"
    assistant_tool "$(ts_add x 120)" "write" "{\"path\":\"src/index.ts\"}" 6000 60 0.018
    tool_result "$(ts_add x 135)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Healthy: balanced read-write pattern" "none" "12"
}

gen_healthy_3_reads_then_write() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-healthy-3r1w.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Add error handling"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*25)))" "read" "{\"path\":\"src/handlers/h$i.ts\"}" "$((3000+i*1000))" 40 "$(echo "scale=6;0.009+$i*0.003" | bc)"
      tool_result "$(ts_add x $((i*25+12)))" "export function h$i() {}"
    done
    assistant_tool "$(ts_add x 100)" "write" "{\"path\":\"src/handlers/h1.ts\"}" 7000 60 0.021
    tool_result "$(ts_add x 115)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Healthy: 3 reads then 1 write" "none" "12"
}

gen_healthy_with_exec() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-healthy-exec.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Run the tests and fix failures"
    assistant_tool "$(ts_add x 30)" "exec" "{\"command\":\"npm test\"}" 3000 40 0.009
    tool_result "$(ts_add x 45)" "FAIL: 2 tests failed"
    assistant_tool "$(ts_add x 60)" "read" "{\"path\":\"src/test.ts\"}" 4000 40 0.012
    tool_result "$(ts_add x 75)" "it('should work', () => {})"
    assistant_tool "$(ts_add x 90)" "write" "{\"path\":\"src/test.ts\"}" 5000 60 0.015
    tool_result "$(ts_add x 105)" "File written"
    assistant_tool "$(ts_add x 120)" "exec" "{\"command\":\"npm test\"}" 6000 40 0.018
    tool_result "$(ts_add x 135)" "PASS: all tests passed"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Healthy: exec-read-write-exec pattern" "none" "12"
}

gen_healthy_many_small_edits() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-healthy-many-edits.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Rename userId to user_id everywhere"
    for i in $(seq 1 8); do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/models/model-$i.ts\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.003+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*30+10)))" "const userId = $i;"
      assistant_tool "$(ts_add x $((i*30+15)))" "write" "{\"path\":\"src/models/model-$i.ts\"}" "$((3500+i*500))" 60 "$(echo "scale=6;0.004+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*30+25)))" "File written"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Healthy: many read-write pairs (no spiral)" "none" "12"
}

# ============================================================================
# CATEGORY 4: Cross-pattern interactions with pattern 12
# ============================================================================

# S18: Compaction damage (pattern 10) + task drift (pattern 12)
gen_compaction_plus_drift() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-compaction-and-drift.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Update the API error handling"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/api/errors/handler-$i.ts\"}" "$((5000+i*3000))" 40 "$(echo "scale=6;0.015+$i*0.009" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export function handleError$i() {}"
    done
    assistant_tool "$(ts_add x 150)" "write" "{\"path\":\"src/api/errors/handler-1.ts\"}" 18000 60 0.054
    tool_result "$(ts_add x 165)" "File written"
    # Compaction
    assistant_text "$(ts_add x 180)" "Compaction triggered." 82000 20 0.246
    assistant_text "$(ts_add x 195)" "Compaction complete." 29000 20 0.087
    # Re-read same file (compaction damage) PLUS drift to new dirs
    assistant_tool "$(ts_add x 210)" "read" "{\"path\":\"src/api/errors/handler-1.ts\"}" 31000 40 0.093
    tool_result "$(ts_add x 225)" "export function handleError1() {}"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((240+i*30)))" "read" "{\"path\":\"src/frontend/views/view-$i.tsx\"}" "$((33000+i*2000))" 40 "$(echo "scale=6;0.099+$i*0.006" | bc)"
      tool_result "$(ts_add x $((240+i*30+15)))" "export const View$i = () => <div/>"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Compaction damage + task drift co-occurring" "10,12" ""
}

# S19: Cost spike + exploration spiral
gen_cost_spike_plus_spiral() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-cost-spike-spiral.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Analyze the codebase"
    for i in $(seq 1 12); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/deep/nested/file-$i.ts\"}" "$((20000+i*5000))" 40 "$(echo "scale=6;0.060+$i*0.015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "// Large file content line $i repeated 500 times..."
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Cost spike + exploration spiral" "6,12" ""
}

# S20: Retry loop — should NOT trigger exploration (retries use exec not read)
gen_retry_no_spiral() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-retry-no-spiral.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Deploy the app"
    for i in $(seq 1 8); do
      assistant_tool "$(ts_add x $((i*20)))" "exec" "{\"command\":\"bash deploy.sh\"}" "$((3000+i*1000))" 40 "$(echo "scale=6;0.009+$i*0.003" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "Error: deployment failed"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Retry loop via exec — should NOT trigger pattern 12" "1" "12"
}

# ============================================================================
# CATEGORY 5: Edge cases
# ============================================================================

# S21: Session with no tool calls at all
gen_edge_no_tools() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-no-tools.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Explain how promises work"
    assistant_text "$(ts_add x 30)" "Promises represent async operations..." 1000 200 0.005
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: no tool calls at all" "none" "12"
}

# S22: Session with only write calls (no reads)
gen_edge_only_writes() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-only-writes.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Create 5 new files"
    for i in $(seq 1 5); do
      assistant_tool "$(ts_add x $((i*30)))" "write" "{\"path\":\"src/new/file-$i.ts\"}" "$((3000+i*500))" 60 "$(echo "scale=6;0.009+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "File written"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: only write calls" "none" "12"
}

# S23: Compaction with no file-path tools (only text + exec)
gen_edge_compaction_no_paths() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-compaction-no-paths.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Help me debug"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "exec" "{\"command\":\"echo test-$i\"}" "$((5000+i*3000))" 40 "$(echo "scale=6;0.015+$i*0.009" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "test-$i"
    done
    assistant_text "$(ts_add x 120)" "Compaction." 75000 20 0.225
    assistant_text "$(ts_add x 135)" "Done." 26000 20 0.078
    for i in 4 5 6; do
      assistant_tool "$(ts_add x $((150+(i-3)*30)))" "exec" "{\"command\":\"echo test-$i\"}" "$((28000+(i-3)*2000))" 40 "$(echo "scale=6;0.084+(($i-3))*0.006" | bc)"
      tool_result "$(ts_add x $((150+(i-3)*30+15)))" "test-$i"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: compaction but no file-path tools" "none" "12"
}

# S24: Very long session with 50 turns, reads interspersed with writes
gen_edge_long_balanced() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-long-balanced.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Refactor the entire module"
    for i in $(seq 1 25); do
      assistant_tool "$(ts_add x $((i*15)))" "read" "{\"path\":\"src/mod/part-$i.ts\"}" "$((3000+i*200))" 40 "$(echo "scale=6;0.003+$i*0.0006" | bc)"
      tool_result "$(ts_add x $((i*15+5)))" "export const p$i = {};"
      assistant_tool "$(ts_add x $((i*15+8)))" "write" "{\"path\":\"src/mod/part-$i.ts\"}" "$((3200+i*200))" 60 "$(echo "scale=6;0.004+$i*0.0006" | bc)"
      tool_result "$(ts_add x $((i*15+12)))" "File written"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: 50 tool calls but balanced read-write" "none" "12"
}

# S25: Multiple compactions in one session
gen_edge_multi_compaction() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-multi-compaction.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Big refactor"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/core/a-$i.ts\"}" "$((5000+i*3000))" 40 "$(echo "scale=6;0.015+$i*0.009" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export const a$i = {};"
    done
    assistant_tool "$(ts_add x 105)" "write" "{\"path\":\"src/core/a-1.ts\"}" 15000 60 0.045
    tool_result "$(ts_add x 120)" "File written"
    # First compaction
    assistant_text "$(ts_add x 135)" "Compaction 1." 80000 20 0.240
    assistant_text "$(ts_add x 150)" "Done." 28000 20 0.084
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((165+i*30)))" "read" "{\"path\":\"src/core/b-$i.ts\"}" "$((30000+i*2000))" 40 "$(echo "scale=6;0.090+$i*0.006" | bc)"
      tool_result "$(ts_add x $((165+i*30+15)))" "export const b$i = {};"
    done
    assistant_tool "$(ts_add x 270)" "write" "{\"path\":\"src/core/b-1.ts\"}" 38000 60 0.114
    tool_result "$(ts_add x 285)" "File written"
    # Second compaction
    assistant_text "$(ts_add x 300)" "Compaction 2." 85000 20 0.255
    assistant_text "$(ts_add x 315)" "Done." 30000 20 0.090
    # Stay in same dir after second compaction
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((330+i*30)))" "read" "{\"path\":\"src/core/c-$i.ts\"}" "$((32000+i*2000))" 40 "$(echo "scale=6;0.096+$i*0.006" | bc)"
      tool_result "$(ts_add x $((330+i*30+15)))" "export const c$i = {};"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: multiple compactions, stays in same dir family" "none" "12"
}

# ============================================================================
# CATEGORY 6: Other patterns — verify no false positive on pattern 12
# ============================================================================

# S26-S36: One fixture per existing pattern, verify pattern 12 does NOT fire

gen_other_pattern() {
  local pattern_num="$1" desc="$2" key="${3:-agent:main:main}" model="${4:-anthropic/claude-sonnet-4-6}"
  N=$((N+1)); local f="s$(printf '%02d' $N)-other-p${pattern_num}.jsonl"

  case "$pattern_num" in
    2) # Non-retryable retry
      {
        session_header "stress-$N" "$model" "$key"
        user_msg "$(ts_add x 0)" "Create a user"
        for i in $(seq 1 4); do
          assistant_tool "$(ts_add x $((i*30)))" "exec" "{\"command\":\"curl -X POST /api/users\"}" "$((3000+i*1000))" 40 "$(echo "scale=6;0.009+$i*0.003" | bc)"
          tool_result "$(ts_add x $((i*30+15)))" "TypeError: Missing required parameter 'name'"
        done
      } > "$OUT_DIR/$f"
      add_manifest "$f" "Other: pattern $pattern_num ($desc)" "$pattern_num" "12"
      ;;
    3) # Tool as text
      {
        session_header "stress-$N" "$model" "$key"
        user_msg "$(ts_add x 0)" "Read my config"
        for i in $(seq 1 3); do
          assistant_text "$(ts_add x $((i*30)))" "read ~/.config/file-$i.yaml" "$((2000+i*500))" 40 "$(echo "scale=6;0.006+$i*0.0015" | bc)"
        done
      } > "$OUT_DIR/$f"
      add_manifest "$f" "Other: pattern $pattern_num ($desc)" "$pattern_num" "12"
      ;;
    5) # Subagent replay
      {
        session_header "stress-$N" "$model" "agent:main:subagent:worker"
        user_msg "$(ts_add x 0)" "Summarize the report"
        for i in $(seq 1 5); do
          assistant_text "$(ts_add x $((i*30)))" "The report shows revenue growth of 15%." "$((2000+i*500))" 60 "$(echo "scale=6;0.006+$i*0.0015" | bc)"
        done
      } > "$OUT_DIR/$f"
      add_manifest "$f" "Other: pattern $pattern_num ($desc)" "$pattern_num" "12"
      ;;
    7) # Skill miss
      {
        session_header "stress-$N" "$model" "$key"
        user_msg "$(ts_add x 0)" "Run the linter"
        assistant_tool "$(ts_add x 30)" "exec" "{\"command\":\"eslint src/\"}" 3000 40 0.009
        tool_result "$(ts_add x 45)" "bash: eslint: command not found"
        assistant_text "$(ts_add x 60)" "ESLint is not installed." 4000 40 0.012
      } > "$OUT_DIR/$f"
      add_manifest "$f" "Other: pattern $pattern_num ($desc)" "$pattern_num" "12"
      ;;
    8) # Model routing waste
      {
        session_header "stress-$N" "anthropic/claude-opus-4-6" "cron:heartbeat"
        user_msg "$(ts_add x 0)" "Check system status"
        assistant_tool "$(ts_add x 30)" "exec" "{\"command\":\"uptime\"}" 3000 40 0.045
        tool_result "$(ts_add x 45)" "up 47 days"
        assistant_text "$(ts_add x 60)" "System is healthy." 4000 30 0.060
      } > "$OUT_DIR/$f"
      add_manifest "$f" "Other: pattern $pattern_num ($desc)" "$pattern_num" "12"
      ;;
    9) # Cron accumulation
      {
        session_header "stress-$N" "anthropic/claude-opus-4-6" "cron:daily-report"
        user_msg "$(ts_add x 0)" "Generate report"
        assistant_text "$(ts_add x 30)" "Run 1." 5000 40 0.015
        assistant_text "$(ts_add x 60)" "Run 2." 12000 40 0.036
        assistant_text "$(ts_add x 90)" "Run 3." 25000 40 0.075
        assistant_text "$(ts_add x 120)" "Run 4." 55000 40 0.165
      } > "$OUT_DIR/$f"
      add_manifest "$f" "Other: pattern $pattern_num ($desc)" "$pattern_num" "12"
      ;;
    11) # Workspace overhead
      {
        session_header "stress-$N" "$model" "$key"
        user_msg "$(ts_add x 0)" "Hello"
        assistant_text "$(ts_add x 30)" "Hi there!" 25000 20 0.075
        assistant_text "$(ts_add x 60)" "How can I help?" 26000 20 0.078
      } > "$OUT_DIR/$f"
      add_manifest "$f" "Other: pattern $pattern_num ($desc)" "$pattern_num" "12"
      ;;
  esac
}

# ============================================================================
# CATEGORY 7: Realistic multi-step workflows (no drift expected)
# ============================================================================

gen_realistic_bugfix() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-realistic-bugfix.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Fix the null pointer in getUserProfile"
    assistant_tool "$(ts_add x 20)" "Grep" "{\"pattern\":\"getUserProfile\",\"path\":\"src/\"}" 3000 40 0.009
    tool_result "$(ts_add x 30)" "src/services/user.ts:42: async function getUserProfile(id)"
    assistant_tool "$(ts_add x 45)" "read" "{\"path\":\"src/services/user.ts\"}" 4000 40 0.012
    tool_result "$(ts_add x 55)" "async function getUserProfile(id) { return db.query(id); }"
    assistant_tool "$(ts_add x 70)" "read" "{\"path\":\"src/services/__tests__/user.test.ts\"}" 5500 40 0.016
    tool_result "$(ts_add x 80)" "it('gets profile', async () => { await getUserProfile(1); });"
    assistant_tool "$(ts_add x 95)" "write" "{\"path\":\"src/services/user.ts\"}" 6500 80 0.020
    tool_result "$(ts_add x 110)" "File written"
    assistant_tool "$(ts_add x 125)" "write" "{\"path\":\"src/services/__tests__/user.test.ts\"}" 7500 60 0.023
    tool_result "$(ts_add x 140)" "File written"
    assistant_tool "$(ts_add x 155)" "exec" "{\"command\":\"npm test -- --testPathPattern=user\"}" 8000 40 0.024
    tool_result "$(ts_add x 170)" "PASS: 3 tests passed"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Realistic: standard bugfix workflow" "none" "12"
}

gen_realistic_feature() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-realistic-feature.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Add pagination to the users API"
    assistant_tool "$(ts_add x 20)" "read" "{\"path\":\"src/api/routes/users.ts\"}" 3000 40 0.009
    tool_result "$(ts_add x 30)" "router.get('/users', getAllUsers)"
    assistant_tool "$(ts_add x 45)" "read" "{\"path\":\"src/api/services/user-service.ts\"}" 4500 40 0.014
    tool_result "$(ts_add x 55)" "async function getAllUsers() { return db.query('SELECT * FROM users'); }"
    assistant_tool "$(ts_add x 70)" "read" "{\"path\":\"src/api/types/pagination.ts\"}" 5500 40 0.017
    tool_result "$(ts_add x 80)" "export interface PaginationParams { page: number; limit: number; }"
    assistant_tool "$(ts_add x 95)" "write" "{\"path\":\"src/api/services/user-service.ts\"}" 7000 100 0.021
    tool_result "$(ts_add x 115)" "File written"
    assistant_tool "$(ts_add x 130)" "write" "{\"path\":\"src/api/routes/users.ts\"}" 8000 80 0.024
    tool_result "$(ts_add x 145)" "File written"
    assistant_tool "$(ts_add x 160)" "write" "{\"path\":\"src/api/__tests__/users.test.ts\"}" 9000 120 0.027
    tool_result "$(ts_add x 180)" "File written"
    assistant_tool "$(ts_add x 195)" "exec" "{\"command\":\"npm test\"}" 10000 40 0.030
    tool_result "$(ts_add x 210)" "PASS: 8 tests passed"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Realistic: feature addition workflow" "none" "12"
}

gen_realistic_refactor() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-realistic-refactor.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Extract the validation logic into a shared module"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((i*25)))" "read" "{\"path\":\"src/api/validators/v$i.ts\"}" "$((3000+i*800))" 40 "$(echo "scale=6;0.009+$i*0.0024" | bc)"
      tool_result "$(ts_add x $((i*25+12)))" "function validate$i(input) { if (!input) throw new Error('invalid'); }"
    done
    assistant_tool "$(ts_add x 120)" "write" "{\"path\":\"src/shared/validation.ts\"}" 7000 120 0.021
    tool_result "$(ts_add x 140)" "File written"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((155+(i-1)*20)))" "write" "{\"path\":\"src/api/validators/v$i.ts\"}" "$((7500+i*500))" 60 "$(echo "scale=6;0.023+$i*0.0015" | bc)"
      tool_result "$(ts_add x $((155+(i-1)*20+10)))" "File written"
    done
    assistant_tool "$(ts_add x 240)" "exec" "{\"command\":\"npm test\"}" 10000 40 0.030
    tool_result "$(ts_add x 255)" "PASS: 12 tests passed"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Realistic: refactor extraction workflow" "none" "12"
}

# ============================================================================
# CATEGORY 8: Stress variants for drift sub-detector A
# ============================================================================

# S33: Drift to 5 different new directories
gen_drift_multi_dir() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-multi-dir.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Fix the payment flow"
    for i in 1 2; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/payments/pay-$i.ts\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export const pay$i = {};"
    done
    assistant_text "$(ts_add x 90)" "Compaction." 78000 20 0.234
    assistant_text "$(ts_add x 105)" "Done." 27000 20 0.081
    assistant_tool "$(ts_add x 120)" "read" "{\"path\":\"src/auth/login.ts\"}" 29000 40 0.087
    tool_result "$(ts_add x 135)" "export const login = {};"
    assistant_tool "$(ts_add x 150)" "read" "{\"path\":\"src/ui/dashboard.tsx\"}" 31000 40 0.093
    tool_result "$(ts_add x 165)" "export const Dashboard = () => <div/>;"
    assistant_tool "$(ts_add x 180)" "read" "{\"path\":\"docs/readme.md\"}" 33000 40 0.099
    tool_result "$(ts_add x 195)" "# README"
    assistant_tool "$(ts_add x 210)" "read" "{\"path\":\"config/settings.yaml\"}" 35000 40 0.105
    tool_result "$(ts_add x 225)" "debug: true"
    assistant_tool "$(ts_add x 240)" "read" "{\"path\":\"scripts/deploy.sh\"}" 37000 40 0.111
    tool_result "$(ts_add x 255)" "#!/bin/bash"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Drift: scattered across 5 new directories" "12" ""
}

# S34: Post-compaction drift with some original dir mixed in (>50% new)
gen_drift_mixed_new_old() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-mixed.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Update user service"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/services/user-$i.ts\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export function user$i() {}"
    done
    assistant_text "$(ts_add x 120)" "Compaction." 76000 20 0.228
    assistant_text "$(ts_add x 135)" "Done." 26000 20 0.078
    # 1 old dir + 4 new dir calls
    assistant_tool "$(ts_add x 150)" "read" "{\"path\":\"src/services/user-4.ts\"}" 28000 40 0.084
    tool_result "$(ts_add x 165)" "export function user4() {}"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((180+i*30)))" "read" "{\"path\":\"src/middleware/mw-$i.ts\"}" "$((30000+i*2000))" 40 "$(echo "scale=6;0.090+$i*0.006" | bc)"
      tool_result "$(ts_add x $((180+i*30+15)))" "export function mw$i() {}"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Drift: 80% new dirs post-compaction (4 new, 1 old)" "12" ""
}

# S35: Post-compaction but 40% new (below 50% threshold)
gen_drift_below_pct() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-below-pct.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Review the auth module"
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/auth/part-$i.ts\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export const auth$i = {};"
    done
    assistant_text "$(ts_add x 150)" "Compaction." 78000 20 0.234
    assistant_text "$(ts_add x 165)" "Done." 27000 20 0.081
    # 3 old dir + 2 new dir (40% new — below 50%)
    for i in 5 6 7; do
      assistant_tool "$(ts_add x $((180+(i-4)*30)))" "read" "{\"path\":\"src/auth/part-$i.ts\"}" "$((29000+(i-4)*2000))" 40 "$(echo "scale=6;0.087+(($i-4))*0.006" | bc)"
      tool_result "$(ts_add x $((180+(i-4)*30+15)))" "export const auth$i = {};"
    done
    for i in 1 2; do
      assistant_tool "$(ts_add x $((270+i*30)))" "read" "{\"path\":\"src/utils/util-$i.ts\"}" "$((35000+i*2000))" 40 "$(echo "scale=6;0.105+$i*0.006" | bc)"
      tool_result "$(ts_add x $((270+i*30+15)))" "export const util$i = {};"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "No drift: 40% new dirs (below 50% threshold)" "none" "12"
}

# ============================================================================
# Generate all fixtures
# ============================================================================

echo "Generating stress test fixtures..."

# Category 1: Drift
gen_drift_classic
gen_drift_docs
gen_drift_borderline
gen_no_drift_same_dirs
gen_no_drift_below_threshold

# Category 2: Exploration spiral
gen_spiral_15
gen_spiral_10
gen_spiral_9
gen_spiral_mixed
gen_spiral_broken_by_exec
gen_spiral_broken_by_write
gen_spiral_glob

# Category 3: Healthy
gen_healthy_short
gen_healthy_read_write_balanced
gen_healthy_3_reads_then_write
gen_healthy_with_exec
gen_healthy_many_small_edits

# Category 4: Cross-pattern
gen_compaction_plus_drift
gen_cost_spike_plus_spiral
gen_retry_no_spiral

# Category 5: Edge cases
gen_edge_no_tools
gen_edge_only_writes
gen_edge_compaction_no_paths
gen_edge_long_balanced
gen_edge_multi_compaction

# Category 6: Other patterns — verify no false positive
gen_other_pattern 2 "non-retryable-retry"
gen_other_pattern 3 "tool-as-text"
gen_other_pattern 5 "subagent-replay"
gen_other_pattern 7 "skill-miss"
gen_other_pattern 8 "model-routing-waste" "cron:heartbeat" "anthropic/claude-opus-4-6"
gen_other_pattern 9 "cron-accumulation" "cron:daily-report" "anthropic/claude-opus-4-6"
gen_other_pattern 11 "workspace-overhead"

# Category 7: Realistic workflows
gen_realistic_bugfix
gen_realistic_feature
gen_realistic_refactor

# Category 8: Drift variants
gen_drift_multi_dir
gen_drift_mixed_new_old
gen_drift_below_pct

# ============================================================================
# CATEGORY 9: Additional edge cases to reach 50+
# ============================================================================

# S39: Exploration spiral ending at session end (no trailing write)
gen_spiral_end_of_session() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-end-session.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "What does the codebase look like?"
    for i in $(seq 1 11); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/module-$i/index.ts\"}" "$((3000+i*400))" 40 "$(echo "scale=6;0.003+$i*0.0012" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "export default {};"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Spiral: 11 reads then session ends (no write)" "12" ""
}

# S40: Drift where agent writes to new dirs (not just reads)
gen_drift_writes_new_dirs() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-writes-new.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Fix the cache layer"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/cache/store-$i.ts\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export const store$i = {};"
    done
    assistant_tool "$(ts_add x 105)" "write" "{\"path\":\"src/cache/store-1.ts\"}" 12000 60 0.036
    tool_result "$(ts_add x 120)" "File written"
    assistant_text "$(ts_add x 135)" "Compaction." 80000 20 0.240
    assistant_text "$(ts_add x 150)" "Done." 28000 20 0.084
    # Drift: writing to completely new directories
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((165+i*30)))" "write" "{\"path\":\"src/logging/logger-$i.ts\"}" "$((30000+i*2000))" 60 "$(echo "scale=6;0.090+$i*0.006" | bc)"
      tool_result "$(ts_add x $((165+i*30+15)))" "File written"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Drift: writes (not reads) to new dirs post-compaction" "12" ""
}

# S41: Very shallow compaction (exactly 40% drop)
gen_edge_shallow_compaction() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-shallow-compact.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Review code"
    assistant_tool "$(ts_add x 30)" "read" "{\"path\":\"src/old/file.ts\"}" 10000 40 0.030
    tool_result "$(ts_add x 45)" "content"
    # Exactly 40% drop: 10000 -> 6000
    assistant_tool "$(ts_add x 60)" "read" "{\"path\":\"src/new/other.ts\"}" 6000 40 0.018
    tool_result "$(ts_add x 75)" "content"
    assistant_tool "$(ts_add x 90)" "read" "{\"path\":\"src/new/another.ts\"}" 6500 40 0.020
    tool_result "$(ts_add x 105)" "content"
    assistant_tool "$(ts_add x 120)" "read" "{\"path\":\"src/new/third.ts\"}" 7000 40 0.021
    tool_result "$(ts_add x 135)" "content"
    assistant_tool "$(ts_add x 150)" "read" "{\"path\":\"src/new/fourth.ts\"}" 7500 40 0.023
    tool_result "$(ts_add x 165)" "content"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: exactly 40% token drop (compaction boundary)" "12" ""
}

# S42: 39% drop — should NOT be treated as compaction
gen_edge_no_compaction_39pct() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-39pct-drop.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Check things"
    assistant_tool "$(ts_add x 30)" "read" "{\"path\":\"src/old/file.ts\"}" 10000 40 0.030
    tool_result "$(ts_add x 45)" "content"
    # 39% drop: 10000 -> 6100 (not enough to be compaction)
    assistant_tool "$(ts_add x 60)" "read" "{\"path\":\"src/new/other.ts\"}" 6100 40 0.018
    tool_result "$(ts_add x 75)" "content"
    assistant_tool "$(ts_add x 90)" "read" "{\"path\":\"src/new/another.ts\"}" 6500 40 0.020
    tool_result "$(ts_add x 105)" "content"
    assistant_tool "$(ts_add x 120)" "read" "{\"path\":\"src/new/third.ts\"}" 7000 40 0.021
    tool_result "$(ts_add x 135)" "content"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: 39% token drop (not compaction)" "none" "12"
}

# S43: Cron session with exploration spiral — should fire both 8/9 and 12
gen_cron_with_spiral() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-cron-spiral.jsonl"
  {
    session_header "stress-$N" "anthropic/claude-opus-4-6" "cron:nightly-scan"
    user_msg "$(ts_add x 0)" "Scan all config files"
    for i in $(seq 1 12); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"/etc/config-$i.yaml\"}" "$((3000+i*500))" 40 "$(echo "scale=6;0.045+$i*0.015" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "setting: value"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Cron + model waste + exploration spiral" "8,12" ""
}

# S44: Session with Unicode in file paths
gen_edge_unicode_paths() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-unicode.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Review translations"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/i18n/locale-$i.json\"}" "$((3000+i*1000))" 40 "$(echo "scale=6;0.009+$i*0.003" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "{\"hello\": \"Hola\"}"
    done
    assistant_tool "$(ts_add x 120)" "write" "{\"path\":\"src/i18n/locale-1.json\"}" 7000 60 0.021
    tool_result "$(ts_add x 135)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: Unicode-adjacent paths, healthy session" "none" "12"
}

# S45: Deep nesting — all files in same deeply nested dir
gen_edge_deep_nesting() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-deep-nest.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Fix tests"
    for i in $(seq 1 8); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/modules/auth/providers/oauth/google/test-$i.ts\"}" "$((3000+i*400))" 40 "$(echo "scale=6;0.003+$i*0.0012" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "test $i"
    done
    assistant_tool "$(ts_add x 180)" "write" "{\"path\":\"src/modules/auth/providers/oauth/google/test-1.ts\"}" 7000 60 0.021
    tool_result "$(ts_add x 195)" "File written"
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: all files in deeply nested same directory" "none" "12"
}

# S46: Drift to same parent dir different child (src/api/v1 → src/api/v2)
gen_drift_sibling_dirs() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-sibling.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Update API v1 endpoints"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":\"src/api/v1/endpoint-$i.ts\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "export function ep$i() {}"
    done
    assistant_text "$(ts_add x 120)" "Compaction." 78000 20 0.234
    assistant_text "$(ts_add x 135)" "Done." 27000 20 0.081
    # Drift to sibling dir v2
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((150+i*30)))" "read" "{\"path\":\"src/api/v2/endpoint-$i.ts\"}" "$((29000+i*2000))" 40 "$(echo "scale=6;0.087+$i*0.006" | bc)"
      tool_result "$(ts_add x $((150+i*30+15)))" "export function ep$i() {}"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Drift: sibling dirs (src/api/v1 → src/api/v2)" "12" ""
}

# S47: 20 reads interspersed with Edit calls (not Write) — Edit breaks spiral
gen_spiral_broken_by_edit() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-edit-break.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Update comments"
    for i in $(seq 1 5); do
      assistant_tool "$(ts_add x $((i*20)))" "read" "{\"path\":\"src/part-$i.ts\"}" "$((3000+i*400))" 40 "$(echo "scale=6;0.003+$i*0.0012" | bc)"
      tool_result "$(ts_add x $((i*20+10)))" "content $i"
    done
    assistant_tool "$(ts_add x 120)" "Edit" "{\"path\":\"src/part-1.ts\"}" 5500 60 0.017
    tool_result "$(ts_add x 135)" "File edited"
    for i in $(seq 6 10); do
      assistant_tool "$(ts_add x $((150+(i-5)*20)))" "read" "{\"path\":\"src/part-$i.ts\"}" "$((6000+(i-5)*400))" 40 "$(echo "scale=6;0.018+(($i-5))*0.0012" | bc)"
      tool_result "$(ts_add x $((150+(i-5)*20+10)))" "content $i"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "No spiral: reads broken by Edit in middle" "none" "12"
}

# S48: Session with null/missing path fields
gen_edge_null_paths() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-edge-null-paths.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Do something"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "read" "{\"path\":null}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "content"
    done
    assistant_text "$(ts_add x 120)" "Compaction." 75000 20 0.225
    assistant_text "$(ts_add x 135)" "Done." 26000 20 0.078
    for i in 4 5 6; do
      assistant_tool "$(ts_add x $((150+(i-3)*30)))" "read" "{}" "$((28000+(i-3)*2000))" 40 "$(echo "scale=6;0.084+(($i-3))*0.006" | bc)"
      tool_result "$(ts_add x $((150+(i-3)*30+15)))" "content"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: null/missing path fields — no crash" "none" "12"
}

# S49: Massive exploration — 30 consecutive reads
gen_spiral_massive() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-spiral-massive.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Audit the entire codebase"
    for i in $(seq 1 30); do
      assistant_tool "$(ts_add x $((i*15)))" "read" "{\"path\":\"src/deep/file-$i.ts\"}" "$((3000+i*300))" 40 "$(echo "scale=6;0.003+$i*0.0009" | bc)"
      tool_result "$(ts_add x $((i*15+7)))" "line $i"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Spiral: massive 30 consecutive reads" "12" ""
}

# S50: Interleaved read-read-write-read-read-write (never hits 10)
gen_healthy_interleaved() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-healthy-interleaved.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Update all handlers"
    for batch in 1 2 3 4; do
      for i in 1 2; do
        local idx=$(( (batch-1)*3 + i ))
        assistant_tool "$(ts_add x $((idx*15)))" "read" "{\"path\":\"src/handlers/h$idx.ts\"}" "$((3000+idx*300))" 40 "$(echo "scale=6;0.003+$idx*0.0009" | bc)"
        tool_result "$(ts_add x $((idx*15+7)))" "handler $idx"
      done
      local widx=$(( batch*3 ))
      assistant_tool "$(ts_add x $((widx*15)))" "write" "{\"path\":\"src/handlers/h$((batch*2-1)).ts\"}" "$((3000+widx*300))" 60 "$(echo "scale=6;0.003+$widx*0.0009" | bc)"
      tool_result "$(ts_add x $((widx*15+7)))" "File written"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Healthy: read-read-write pattern repeating" "none" "12"
}

# S51: Drift where pre-compaction has no file-path tools at all (only exec)
gen_drift_no_pre_paths() {
  N=$((N+1)); local f="s$(printf '%02d' $N)-drift-no-pre-paths.jsonl"
  {
    session_header "stress-$N"
    user_msg "$(ts_add x 0)" "Set up the environment"
    for i in 1 2 3; do
      assistant_tool "$(ts_add x $((i*30)))" "exec" "{\"command\":\"npm install package-$i\"}" "$((5000+i*2000))" 40 "$(echo "scale=6;0.015+$i*0.006" | bc)"
      tool_result "$(ts_add x $((i*30+15)))" "installed package-$i"
    done
    assistant_text "$(ts_add x 120)" "Compaction." 76000 20 0.228
    assistant_text "$(ts_add x 135)" "Done." 26000 20 0.078
    for i in 1 2 3 4; do
      assistant_tool "$(ts_add x $((150+i*30)))" "read" "{\"path\":\"src/new-dir/file-$i.ts\"}" "$((28000+i*2000))" 40 "$(echo "scale=6;0.084+$i*0.006" | bc)"
      tool_result "$(ts_add x $((150+i*30+15)))" "content"
    done
  } > "$OUT_DIR/$f"
  add_manifest "$f" "Edge: no file-path tools pre-compaction, reads post" "none" "12"
}

gen_spiral_end_of_session
gen_drift_writes_new_dirs
gen_edge_shallow_compaction
gen_edge_no_compaction_39pct
gen_cron_with_spiral
gen_edge_unicode_paths
gen_edge_deep_nesting
gen_drift_sibling_dirs
gen_spiral_broken_by_edit
gen_edge_null_paths
gen_spiral_massive
gen_healthy_interleaved
gen_drift_no_pre_paths

echo ""
echo "Generated $N fixtures in $OUT_DIR/"
echo "Manifest: $MANIFEST"
echo ""
cat "$MANIFEST" | column -t -s$'\t'
