#!/bin/bash
# run-daily.sh — Skill Evolver v2.0 Daily Pipeline
#
# Runs one evolution loop: extract → generate → validate → unit-lifecycle
#
# Usage:
#   ./run-daily.sh [options]
#
# Options:
#   --sessions-dir <path>   Session JSONL directory (auto-detect if omitted)
#   --eu-dir <path>         Evolution Unit storage (default: ./eu)
#                           (--patches-dir also accepted as legacy alias)
#   --model <provider/model> LLM model (default: auto-detect)
#   --since <ISO>           Only process sessions after this timestamp (incremental)
#   --window-days N         Fallback: process sessions from last N days (default: 7)
#   --max-si N              Max SIs per run (default: 20)
#   --state <path>          evolver-state.json path (for reading/updating state)
#   --skip-inline           Skip SKILL.md writes
#
# Exit codes:
#   0: success (including "no traces")
#   1: error in pipeline step

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="${SCRIPT_DIR}/.."

# Defaults
SESSIONS_DIR="${OPENCLAW_SESSIONS_DIR:-}"
UNITS_DIR="${WORK_DIR}/eu"
MODEL=""
SINCE=""
WINDOW_DAYS=7
WINDOW_DAYS_EXPLICIT=""
MAX_SI=20
SEP_QUEUE="${WORK_DIR}/sep-queue.jsonl"
SKIP_INLINE=""
STATE_FILE=""
NO_STATE_UPDATE=""
SKIP_SI=0
FILTER_SKILL=""
HINT=""

# Generate run ID for event correlation
export EVOLVER_RUN_ID="$(node -e 'console.log(require("crypto").randomUUID())')"
echo "[run-daily] EVOLVER_RUN_ID=$EVOLVER_RUN_ID"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --sessions-dir) SESSIONS_DIR="$2"; shift 2 ;;
    --eu-dir|--patches-dir)  UNITS_DIR="$2"; shift 2 ;;
    --model)        MODEL="$2"; shift 2 ;;
    --since)        SINCE="$2"; shift 2 ;;
    --window-days)  WINDOW_DAYS="$2"; WINDOW_DAYS_EXPLICIT="1"; shift 2 ;;
    --max-si)       MAX_SI="$2"; shift 2 ;;
    --sep-queue)    SEP_QUEUE="$2"; shift 2 ;;
    --state)        STATE_FILE="$2"; shift 2 ;;
    --skip-inline)  SKIP_INLINE="--skip-inline"; shift ;;
    --no-state-update) NO_STATE_UPDATE="1"; shift ;;
    --skip-si)      SKIP_SI="$2"; shift 2 ;;
    --filter-skill) FILTER_SKILL="$2"; shift 2 ;;
    --hint)         HINT="$2"; shift 2 ;;
    --help)
      echo "Usage: run-daily.sh [--sessions-dir <path>] [--eu-dir <path>] [--model <p/m>] [--since <ISO>] [--max-si N] [--state <path>] [--skip-inline] [--no-state-update] [--filter-skill <name>] [--hint <text>]"
      exit 0 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Auto-detect sessions dir via platform adapter (cross-platform)
if [[ -z "$SESSIONS_DIR" ]]; then
  # Adapter may return multiple dirs (e.g. split by channel).
  # Collect all, join with comma for trace-extractor multi-dir support.
  SESSIONS_DIR=$(node -e "
    const {getAdapter} = require('${SCRIPT_DIR}/lib/platform-detect');
    const paths = getAdapter().detectPaths().filter(p => {
      try { return require('fs').statSync(p).isDirectory(); } catch { return false; }
    });
    if (paths.length) console.log(paths.join(','));
  " 2>/dev/null || true)

  # Fallback: legacy OpenClaw hardcoded paths
  if [[ -z "$SESSIONS_DIR" ]]; then
    _OC_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
    for candidate in \
      "$_OC_ROOT/agents/main/sessions" \
      "$HOME/.openclaw/agents/main/sessions" \
      ; do
      if [[ -d "$candidate" ]]; then
        SESSIONS_DIR="$candidate"
        break
      fi
    done
  fi

  if [[ -z "$SESSIONS_DIR" ]]; then
    echo "[run-daily] ERROR: Cannot find sessions dir (platform adapter + legacy paths all failed)" >&2
    exit 1
  fi
fi

mkdir -p "$UNITS_DIR"

# Read state for --since if state file exists and --since not given
# Skip if --window-days was explicitly passed (user wants windowed lookup, not incremental)
if [[ -z "$SINCE" && -z "$WINDOW_DAYS_EXPLICIT" && -n "$STATE_FILE" && -f "$STATE_FILE" ]]; then
  SINCE=$(node -e "const s=JSON.parse(require('fs').readFileSync('$STATE_FILE','utf8')); if(s.last_evolution_ts) console.log(s.last_evolution_ts)" 2>/dev/null || true)
fi

# Cold start: no state → use window-days 7
if [[ -z "$SINCE" && -n "$STATE_FILE" && ! -f "$STATE_FILE" ]]; then
  WINDOW_DAYS=7
  echo "[run-daily] Cold start: using ${WINDOW_DAYS}d window" >&2
fi

# Build extraction args
EXTRACT_ARGS="--sessions-dir \"$SESSIONS_DIR\" --max-si $MAX_SI"
if [[ -n "$SINCE" ]]; then
  EXTRACT_ARGS="$EXTRACT_ARGS --since $SINCE"
else
  EXTRACT_ARGS="$EXTRACT_ARGS --window-days $WINDOW_DAYS"
fi
if [[ "$SKIP_SI" -gt 0 ]]; then
  EXTRACT_ARGS="$EXTRACT_ARGS --skip-si $SKIP_SI"
fi
if [[ -n "$FILTER_SKILL" ]]; then
  # Push --filter-skill down to the extractor so --max-si counts only matching SIs.
  EXTRACT_ARGS="$EXTRACT_ARGS --filter-skill $FILTER_SKILL"
fi

# Temp files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TRACES_FILE="/tmp/evolver_traces_${TIMESTAMP}.jsonl"
EVIDENCE_FILE="/tmp/evolver_evidence_${TIMESTAMP}.jsonl"
REPORT_FILE="${UNITS_DIR}/evolution-report.json"

MODEL_ARG=""
[[ -n "$MODEL" ]] && MODEL_ARG="--model $MODEL"

START_TIME=$(date +%s)

echo "============================================" >&2
echo "[run-daily] Skill Evolver v2.0 Pipeline" >&2
echo "[run-daily] $(date -Iseconds)" >&2
echo "[run-daily] sessions: $SESSIONS_DIR" >&2
echo "[run-daily] units:    $UNITS_DIR" >&2
if [[ -n "$SINCE" ]]; then
  echo "[run-daily] source:   since $SINCE" >&2
else
  echo "[run-daily] source:   ${WINDOW_DAYS}d window" >&2
fi
echo "[run-daily] max-si:   $MAX_SI" >&2
echo "[run-daily] model:    ${MODEL:-auto}" >&2
echo "============================================" >&2

STEP_FAILED=""
handle_error() { STEP_FAILED="$1"; echo "[run-daily] ERROR in ${1}" >&2; }

# ─── Step 1: Extract Traces ─────────────────────────────────────

echo "" >&2
echo ">>> Step 1: Extract traces" >&2
if ! eval node "${SCRIPT_DIR}/trace-extractor.js" $EXTRACT_ARGS --output "$TRACES_FILE"; then
  handle_error "trace-extractor"
fi

TRACE_COUNT=$(wc -l < "$TRACES_FILE" 2>/dev/null | tr -d ' ' || echo 0)
echo "[run-daily] Extracted ${TRACE_COUNT} traces" >&2

# ─── Step 1.5: Optional hint injection ────────────────────────
# Filtering by skill is now done inside trace-extractor (see EXTRACT_ARGS
# build) so that --max-si counts only matching SIs. This step only handles
# --hint, which prepends a "### User Hint" block to each SI.trace; the
# generator's LLM uses it as steering when extracting Evolution Units.
if [[ -n "$HINT" ]]; then
  echo "[run-daily] Step 1.5: hint=<provided>" >&2
  HINT="$HINT" TRACES_FILE="$TRACES_FILE" node -e '
    const fs = require("fs");
    const hint = process.env.HINT || "";
    const tracesFile = process.env.TRACES_FILE;
    const lines = fs.readFileSync(tracesFile, "utf8").split("\n").filter(Boolean);
    const out = [];
    for (const l of lines) {
      let si;
      try { si = JSON.parse(l); } catch { continue; }
      si.trace = `### User Hint\n${hint}\n\n### Original Trace\n${si.trace || ""}`;
      out.push(JSON.stringify(si));
    }
    fs.writeFileSync(tracesFile, out.join("\n") + (out.length ? "\n" : ""));
    console.error(`[run-daily] After hint injection: ${out.length} SIs`);
  ' || { echo "[run-daily] Step 1.5 failed" >&2; exit 1; }
  TRACE_COUNT=$(wc -l < "$TRACES_FILE" 2>/dev/null | tr -d ' ' || echo 0)
fi

if [[ "$TRACE_COUNT" -eq 0 ]]; then
  echo "[run-daily] No traces found." >&2
  END_TIME=$(date +%s)
  cat > "$REPORT_FILE" << REPORT
{"timestamp":"$(date -Iseconds)","duration_s":$((END_TIME-START_TIME)),"traces":0,"result":"no_traces"}
REPORT
  rm -f "$TRACES_FILE"
  exit 0
fi

# ─── Step 2: Generate Patches ───────────────────────────────────

echo "" >&2
echo ">>> Step 2: Generate units" >&2
GEN_LOG="/tmp/evolver_generator_${TIMESTAMP}.log"
if ! node "${SCRIPT_DIR}/generator.js" \
  --traces "$TRACES_FILE" \
  --eu-dir "$UNITS_DIR" \
  --sep-queue "$SEP_QUEUE" \
  $MODEL_ARG 2> >(tee "$GEN_LOG" >&2); then
  handle_error "generator"
fi

# ─── Step 3: Validate ───────────────────────────────────────────

echo "" >&2
echo ">>> Step 3: Validate units" >&2

PATCH_COUNT=$(find "$UNITS_DIR" -name "*.md" ! -name "*.superseded.*" ! -name "*.evicted.*" ! -name ".gitkeep" 2>/dev/null | wc -l | tr -d ' ')

VAL_LOG="/tmp/evolver_validator_${TIMESTAMP}.log"
if [[ "$PATCH_COUNT" -eq 0 ]]; then
  echo "[run-daily] No units to validate." >&2
  echo "" > "$EVIDENCE_FILE"
  echo "" > "$VAL_LOG"
else
  if ! node "${SCRIPT_DIR}/validator.js" \
    --traces "$TRACES_FILE" \
    --eu-dir "$UNITS_DIR" \
    --output "$EVIDENCE_FILE" \
    $MODEL_ARG 2> >(tee "$VAL_LOG" >&2); then
    handle_error "validator"
  fi
fi

# ─── Step 4: Patch lifecycle ────────────────────────────────────

echo "" >&2
echo ">>> Step 4: Unit lifecycle (score/promote/evict/inline)" >&2
TRACES_HISTORY_FILE="${WORK_DIR}/traces-history.jsonl"
PATCHER_OUTPUT=""
if ! PATCHER_OUTPUT=$(node "${SCRIPT_DIR}/lifecycle.js" \
  --eu-dir "$UNITS_DIR" \
  --evidence "$EVIDENCE_FILE" \
  --traces "$TRACES_FILE" \
  --traces-history "$TRACES_HISTORY_FILE" \
  --sep-queue "$SEP_QUEUE" \
  $SKIP_INLINE); then
  handle_error "patcher"
fi

# Step 4.5: Append lightweight traces to rolling history (for efficiency stats).
# Keep only { si_id, skill, trace_steps, ts } per trace. Roll 60 days.
#
# IMPORTANT: This step must run AFTER lifecycle.js, not before.
# Including this run's traces in the efficiency baseline would let a unit's
# own traces define its "historical median", inflating or deflating the score
# against itself. Patcher reads the PRE-append history file; the new traces
# only become visible starting from the next run.
#
# Paths are passed via env vars (not shell string interpolation) to avoid
# JS-string injection when filenames contain quotes or backslashes.
if [[ -f "$TRACES_FILE" ]]; then
  TRACES_FILE="$TRACES_FILE" TRACES_HISTORY_FILE="$TRACES_HISTORY_FILE" node -e '
    const fs = require("fs");
    const tracesPath = process.env.TRACES_FILE;
    const histPath = process.env.TRACES_HISTORY_FILE;
    const cutoff = Date.now() - 60*24*3600*1000;
    const lines = fs.readFileSync(tracesPath, "utf8").trim().split("\n").filter(Boolean);
    const appended = lines.map(l => {
      try {
        const e = JSON.parse(l);
        return JSON.stringify({ si_id: e.si_id, skill: e.skill, trace_steps: e.trace_steps, ts: e.end_ts });
      } catch { return null; }
    }).filter(Boolean);
    let existing = [];
    if (fs.existsSync(histPath)) {
      existing = fs.readFileSync(histPath, "utf8").trim().split("\n").filter(Boolean).filter(l => {
        try { return new Date(JSON.parse(l).ts).getTime() > cutoff; } catch { return false; }
      });
    }
    fs.writeFileSync(histPath, [...existing, ...appended].join("\n") + "\n");
    console.error("[run-daily] traces-history: " + (existing.length + appended.length) + " entries (+" + appended.length + " this run)");
  ' >&2 || echo "[run-daily] traces-history update skipped (see error above)" >&2
fi

# Step 4.6: Persist this run's evidence into rolling evidence.jsonl.
# Rationale: validator writes to a /tmp file that patcher consumes and discards.
# brief-data.js needs cross-day evidence to separate "effective/degrade signals"
# from raw traces. Roll 60 days to cap growth.
PERSISTENT_EVIDENCE_FILE="${WORK_DIR}/evidence.jsonl"
if [[ -f "$EVIDENCE_FILE" ]]; then
  EVIDENCE_FILE="$EVIDENCE_FILE" PERSISTENT_EVIDENCE_FILE="$PERSISTENT_EVIDENCE_FILE" node -e '
    const fs = require("fs");
    const src = process.env.EVIDENCE_FILE;
    const dst = process.env.PERSISTENT_EVIDENCE_FILE;
    const cutoff = Date.now() - 60*24*3600*1000;
    const newLines = fs.readFileSync(src, "utf8").trim().split("\n").filter(Boolean);
    if (newLines.length === 0) { console.error("[run-daily] evidence.jsonl: no new entries"); process.exit(0); }
    let existing = [];
    if (fs.existsSync(dst)) {
      existing = fs.readFileSync(dst, "utf8").trim().split("\n").filter(Boolean).filter(l => {
        try { const e = JSON.parse(l); const t = e.date ? new Date(e.date).getTime() : Date.now(); return t > cutoff; } catch { return false; }
      });
    }
    fs.writeFileSync(dst, [...existing, ...newLines].join("\n") + "\n");
    console.error("[run-daily] evidence.jsonl: " + (existing.length + newLines.length) + " entries (+" + newLines.length + " this run)");
  ' >&2 || echo "[run-daily] evidence.jsonl update skipped (see error above)" >&2
fi

# ─── Report ─────────────────────────────────────────────────────

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [[ -n "$PATCHER_OUTPUT" ]]; then
  node -e "
    const p = JSON.parse(process.argv[1]);
    const r = { ...p, pipeline: { duration_s: ${DURATION}, traces: ${TRACE_COUNT}, source: '${SINCE:-window_${WINDOW_DAYS}d}', error: '${STEP_FAILED}' || null }};
    process.stdout.write(JSON.stringify(r, null, 2));
  " "$PATCHER_OUTPUT" > "$REPORT_FILE" 2>/dev/null || echo "$PATCHER_OUTPUT" > "$REPORT_FILE"
else
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"pipeline\":{\"duration_s\":${DURATION},\"error\":\"${STEP_FAILED}\"}}" > "$REPORT_FILE"
fi

# ─── Update State ───────────────────────────────────────────────
# Skip when called from monitor.js (--no-state-update) — monitor manages state itself.

if [[ -n "$STATE_FILE" && -z "$NO_STATE_UPDATE" ]]; then
  node -e "
    const fs = require('fs');
    const p = '${STATE_FILE}';
    let s = {};
    try { s = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
    s.last_evolution_ts = new Date().toISOString();
    s.total_evolutions = (s.total_evolutions || 0) + 1;
    s.total_si_processed = (s.total_si_processed || 0) + ${TRACE_COUNT};
    fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\\n');
  " 2>/dev/null || true
elif [[ -n "$NO_STATE_UPDATE" ]]; then
  echo "[run-daily] State update skipped (managed by caller)" >&2
fi

echo "" >&2
echo "============================================" >&2
echo "[run-daily] Pipeline complete (${DURATION}s)" >&2
echo "[run-daily] Traces: ${TRACE_COUNT} | Report: $REPORT_FILE" >&2
[[ -n "$STEP_FAILED" ]] && echo "[run-daily] ⚠️  Error in: $STEP_FAILED" >&2
echo "============================================" >&2

# ─── Notification (stdout) ──────────────────────────────────────

# Generate notification to stdout (picked up by cron delivery or caller)
if [[ -z "$STEP_FAILED" && "$TRACE_COUNT" -gt 0 ]]; then
  node "${SCRIPT_DIR}/notify.js" \
    --report "$REPORT_FILE" \
    --eu-dir "$UNITS_DIR" \
    --evidence "$EVIDENCE_FILE" \
    --gen-log "$GEN_LOG" \
    --val-log "$VAL_LOG" \
    --traces "$TRACE_COUNT" \
    --duration "$DURATION" \
    2>/dev/null || true
fi

[[ -z "$STEP_FAILED" ]]
