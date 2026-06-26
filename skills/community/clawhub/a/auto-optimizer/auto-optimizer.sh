#!/usr/bin/env bash
# =============================================================================
# auto-optimizer.sh — Universal Optimization Loop
# Combines Karpathy's scalar autoresearch with Rayo's binary eval framework.
# Includes hypothesis memory to prevent retrying failed approaches.
#
# Usage (scalar mode — hard metrics):
#   ./auto-optimizer.sh --metric "cmd" --file "path/to/file" [--budget 20]
#
# Usage (binary mode — soft domains):
#   ./auto-optimizer.sh --eval-mode binary --evals ./evals.md --file "path/to/file"
#
# Requirements: git, claude CLI (or fallback), bc, jq (for hypothesis log)
# =============================================================================

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Wizard Mode ───────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--wizard" ]]; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║              🔧 Auto-Optimizer Setup Wizard                  ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "What do you want to optimize?"
  echo "  1) Cold outreach / email copy"
  echo "  2) LLM prompt / system prompt"
  echo "  3) Prediction market strategy"
  echo "  4) Code / config file"
  echo "  5) Custom (bring your own)"
  echo ""
  read -r -p "Choice [1-5]: " CHOICE

  read -r -p "Path to file you want to optimize: " WIZARD_FILE
  read -r -p "Budget (iterations, default 10): " WIZARD_BUDGET
  WIZARD_BUDGET="${WIZARD_BUDGET:-10}"

  WIZARD_ARGS="--file $WIZARD_FILE --budget $WIZARD_BUDGET"

  case "$CHOICE" in
    1)
      echo ""
      echo "Setting up binary eval mode for outreach optimization."
      EVALS_PATH="/tmp/wizard-outreach-evals.md"
      cat > "$EVALS_PATH" <<'EVEOF'
1. Is the subject line under 10 words?
2. Is the hook (first sentence) under 15 words?
3. Is there exactly one call-to-action?
4. Does the email mention a specific outcome or number?
5. Is the total body under 150 words?
6. Does it address a specific pain point of the recipient?
EVEOF
      echo "Evals written to $EVALS_PATH"
      echo "Running: $0 --eval-mode binary --evals $EVALS_PATH $WIZARD_ARGS"
      exec "$0" --eval-mode binary --evals "$EVALS_PATH" $WIZARD_ARGS
      ;;
    2)
      echo ""
      echo "Setting up binary eval mode for prompt optimization."
      EVALS_PATH="/tmp/wizard-prompt-evals.md"
      cat > "$EVALS_PATH" <<'EVEOF'
1. Does the prompt specify a clear role or persona?
2. Does it include explicit output format instructions?
3. Does it define what NOT to do?
4. Is it under 500 words?
5. Does it include at least one concrete example?
EVEOF
      echo "Evals written to $EVALS_PATH"
      echo "Running: $0 --eval-mode binary --evals $EVALS_PATH $WIZARD_ARGS"
      exec "$0" --eval-mode binary --evals "$EVALS_PATH" $WIZARD_ARGS
      ;;
    3)
      echo ""
      echo "Setting up scalar mode for prediction strategy optimization."
      METRIC_PATH="/tmp/wizard-prediction-metric.sh"
      cat > "$METRIC_PATH" <<'METEOF'
#!/usr/bin/env bash
# Mock prediction metric — replace with real eval
# Scores the strategy file on specificity, base rates, calibration
FILE="${1:-./strategy.md}"
WORDS=$(wc -w < "$FILE" 2>/dev/null || echo 0)
HAS_BASERATES=$(grep -ci "base rate\|historical\|prior" "$FILE" 2>/dev/null || echo 0)
HAS_CALIBRATION=$(grep -ci "calibrat\|confident\|uncertain" "$FILE" 2>/dev/null || echo 0)
HAS_CRITERIA=$(grep -ci "criteri\|threshold\|signal" "$FILE" 2>/dev/null || echo 0)
# Score: more specific = better, but not too long
SCORE=$(echo "scale=4; ($HAS_BASERATES * 20 + $HAS_CALIBRATION * 20 + $HAS_CRITERIA * 20 + [[ $WORDS -gt 50 && $WORDS -lt 500 ]] && echo 40 || echo 0)" | bc -l 2>/dev/null || echo "0.5")
echo "$SCORE"
METEOF
      chmod +x "$METRIC_PATH"
      read -r -p "Minimize or maximize? (min/max, default max): " GOAL_INPUT
      GOAL_INPUT="${GOAL_INPUT:-max}"
      GOAL_FLAG="maximize"
      [[ "$GOAL_INPUT" == "min"* ]] && GOAL_FLAG="minimize"
      echo "Running: $0 --metric 'bash $METRIC_PATH' --goal $GOAL_FLAG $WIZARD_ARGS"
      exec "$0" --metric "bash $METRIC_PATH" --goal "$GOAL_FLAG" $WIZARD_ARGS
      ;;
    4)
      echo ""
      read -r -p "Enter your metric command (must output a float): " WIZARD_METRIC
      read -r -p "Minimize or maximize? (min/max, default max): " GOAL_INPUT
      GOAL_INPUT="${GOAL_INPUT:-max}"
      GOAL_FLAG="maximize"
      [[ "$GOAL_INPUT" == "min"* ]] && GOAL_FLAG="minimize"
      echo "Running: $0 --metric '$WIZARD_METRIC' --goal $GOAL_FLAG $WIZARD_ARGS"
      exec "$0" --metric "$WIZARD_METRIC" --goal "$GOAL_FLAG" $WIZARD_ARGS
      ;;
    5)
      echo ""
      echo "Custom mode. Choose eval type:"
      echo "  s) Scalar (metric command that outputs a float)"
      echo "  b) Binary (yes/no eval criteria file)"
      read -r -p "Type [s/b]: " EVAL_TYPE
      if [[ "$EVAL_TYPE" == "b"* ]]; then
        read -r -p "Path to evals.md file: " WIZARD_EVALS
        exec "$0" --eval-mode binary --evals "$WIZARD_EVALS" $WIZARD_ARGS
      else
        read -r -p "Metric command (outputs a float): " WIZARD_METRIC
        read -r -p "Goal (minimize/maximize): " GOAL_FLAG
        GOAL_FLAG="${GOAL_FLAG:-maximize}"
        exec "$0" --metric "$WIZARD_METRIC" --goal "$GOAL_FLAG" $WIZARD_ARGS
      fi
      ;;
    *)
      echo "Invalid choice. Run with --wizard again."
      exit 1
      ;;
  esac
fi

# ── Demo Mode ─────────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--demo" ]]; then
  DEMO_TYPE="${2:-outreach}"
  DEMO_BUDGET="5"
  DEMO_EVAL_MODE="scalar"
  # Parse remaining args
  shift 2 || true
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --budget)    DEMO_BUDGET="$2"; shift 2 ;;
      --eval-mode) DEMO_EVAL_MODE="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║              🚀 Auto-Optimizer Demo: $DEMO_TYPE              "
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""

  case "$DEMO_TYPE" in
    outreach)
      DEMO_DIR="/tmp/demo-outreach-$$"
      mkdir -p "$DEMO_DIR"
      cd "$DEMO_DIR"
      git init -q && git config user.email "demo@auto-optimizer" && git config user.name "Auto-Optimizer Demo"

      cat > "$DEMO_DIR/outreach.md" <<'TMPLEOF'
Subject: Quick question about [Company]

Hi [Name],

I wanted to reach out because I've been following [Company]'s work and think there might be a great opportunity for us to collaborate.

We help companies like yours improve their sales process using AI-powered outreach tools. Our clients typically see a 3x improvement in reply rates within the first month.

Would you be open to a 15-minute call next week to explore if this could be valuable for [Company]? I'm also happy to share a few case studies from companies similar to yours if that would be helpful.

Looking forward to hearing from you,
[Your Name]
TMPLEOF

      cat > "$DEMO_DIR/metric.sh" <<'METRICEOF'
#!/usr/bin/env bash
# Outreach scorer: 0-100 based on best practices
FILE="${1:-./outreach.md}"
CONTENT=$(cat "$FILE" 2>/dev/null || echo "")
SCORE=0

# Hook under 15 words (first line after Subject:)
HOOK=$(echo "$CONTENT" | grep -v "^Subject:" | grep -v "^$" | head -1)
HOOK_WORDS=$(echo "$HOOK" | wc -w | tr -d ' ')
[[ "$HOOK_WORDS" -le 15 ]] && SCORE=$((SCORE + 25))

# Single CTA (count question marks)
QMARKS=$(echo "$CONTENT" | grep -o "?" | wc -l | tr -d ' ')
[[ "$QMARKS" -eq 1 ]] && SCORE=$((SCORE + 25))

# Body under 120 words
WORDS=$(echo "$CONTENT" | wc -w | tr -d ' ')
[[ "$WORDS" -le 120 ]] && SCORE=$((SCORE + 25))

# Contains specific value/number
echo "$CONTENT" | grep -qE '[0-9]+[x%]|[0-9]+ (percent|times|minutes|days)' && SCORE=$((SCORE + 25))

echo "$SCORE"
METRICEOF
      chmod +x "$DEMO_DIR/metric.sh"

      git add . && git commit -q -m "baseline"

      echo "Demo files created in $DEMO_DIR"
      echo "Running $DEMO_BUDGET iterations..."
      echo ""
      exec "$0" \
        --file "$DEMO_DIR/outreach.md" \
        --metric "bash $DEMO_DIR/metric.sh $DEMO_DIR/outreach.md" \
        --budget "$DEMO_BUDGET" \
        --session "demo-outreach-$$"
      ;;

    prediction)
      DEMO_DIR="/tmp/demo-prediction-$$"
      mkdir -p "$DEMO_DIR"
      cd "$DEMO_DIR"
      git init -q && git config user.email "demo@auto-optimizer" && git config user.name "Auto-Optimizer Demo"

      cat > "$DEMO_DIR/strategy.md" <<'STRATEOF'
# Prediction Strategy

When evaluating prediction markets, look for clear yes/no outcomes.

Consider the available information and make a judgment call about likelihood.

Bet when you feel confident.
STRATEOF

      cat > "$DEMO_DIR/metric.sh" <<'METRICEOF'
#!/usr/bin/env bash
# Prediction strategy scorer: higher = better calibration
FILE="${1:-./strategy.md}"
CONTENT=$(cat "$FILE" 2>/dev/null || echo "")
SCORE=0

# Has base rates / historical reference
echo "$CONTENT" | grep -qiE "base rate|historical|prior|base-rate" && SCORE=$((SCORE + 20))

# Has calibration language
echo "$CONTENT" | grep -qiE "calibrat|confident|uncertain|probability|likelihood" && SCORE=$((SCORE + 20))

# Has specific criteria / thresholds
echo "$CONTENT" | grep -qiE "threshold|signal|criteri|only (bet|trade) when" && SCORE=$((SCORE + 20))

# Has risk management
echo "$CONTENT" | grep -qiE "risk|kelly|position size|stake|bankroll" && SCORE=$((SCORE + 20))

# Sufficiently detailed (>100 words)
WORDS=$(echo "$CONTENT" | wc -w | tr -d ' ')
[[ "$WORDS" -gt 100 ]] && SCORE=$((SCORE + 20))

echo "$SCORE"
METRICEOF
      chmod +x "$DEMO_DIR/metric.sh"

      git add . && git commit -q -m "baseline"

      echo "Demo files created in $DEMO_DIR"
      echo "Running $DEMO_BUDGET iterations..."
      echo ""
      exec "$0" \
        --file "$DEMO_DIR/strategy.md" \
        --metric "bash $DEMO_DIR/metric.sh $DEMO_DIR/strategy.md" \
        --budget "$DEMO_BUDGET" \
        --session "demo-prediction-$$"
      ;;

    prompt)
      DEMO_DIR="/tmp/demo-prompt-$$"
      mkdir -p "$DEMO_DIR"
      cd "$DEMO_DIR"
      git init -q && git config user.email "demo@auto-optimizer" && git config user.name "Auto-Optimizer Demo"

      cat > "$DEMO_DIR/system-prompt.md" <<'PROMPTEOF'
You are a helpful assistant. Answer questions clearly and accurately.
Be concise but thorough. Help the user accomplish their goals.
PROMPTEOF

      cat > "$DEMO_DIR/evals.md" <<'EVALSEOF'
1. Does the prompt specify a clear role or persona (e.g., "You are a [specific role]...")?
2. Does it include explicit output format instructions (e.g., "Respond in bullet points", "Output JSON", etc.)?
3. Does it define at least one constraint on what NOT to do?
4. Is it under 500 words total?
5. Does it include at least one concrete example of desired behavior or output?
EVALSEOF

      git add . && git commit -q -m "baseline"

      echo "Demo files created in $DEMO_DIR"
      echo "Running $DEMO_BUDGET iterations in binary eval mode..."
      echo ""
      exec "$0" \
        --eval-mode binary \
        --file "$DEMO_DIR/system-prompt.md" \
        --evals "$DEMO_DIR/evals.md" \
        --batch-size 5 \
        --budget "$DEMO_BUDGET" \
        --session "demo-prompt-$$"
      ;;

    *)
      echo "Unknown demo type: $DEMO_TYPE"
      echo "Available: outreach, prediction, prompt"
      exit 1
      ;;
  esac
fi

# ── Defaults ─────────────────────────────────────────────────────────────────
METRIC_CMD=""
MUTABLE_FILE=""
BUDGET=20
SESSION_NAME="auto-optimizer-$(date +%Y%m%d-%H%M%S)"
GOAL="maximize"
PROGRAM_FILE=""
EVAL_MODE="scalar"
EVALS_FILE=""
BATCH_SIZE=""

# ── Parse args ────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --metric)     METRIC_CMD="$2";   shift 2 ;;
    --file)       MUTABLE_FILE="$2"; shift 2 ;;
    --budget)     BUDGET="$2";       shift 2 ;;
    --session)    SESSION_NAME="$2"; shift 2 ;;
    --goal)       GOAL="$2";         shift 2 ;;
    --program)    PROGRAM_FILE="$2"; shift 2 ;;
    --eval-mode)  EVAL_MODE="$2";    shift 2 ;;
    --evals)      EVALS_FILE="$2";   shift 2 ;;
    --batch-size) BATCH_SIZE="$2";   shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# ── Set batch size default based on mode ─────────────────────────────────────
if [[ -z "$BATCH_SIZE" ]]; then
  if [[ "$EVAL_MODE" == "binary" ]]; then
    BATCH_SIZE=10
  else
    BATCH_SIZE=1
  fi
fi

# ── Validate ──────────────────────────────────────────────────────────────────
if [[ -z "$MUTABLE_FILE" ]]; then
  echo "ERROR: --file is required."
  echo "Usage: $0 --file <path> [--eval-mode binary|scalar] [--metric cmd] [--evals path]"
  exit 1
fi

if [[ "$EVAL_MODE" == "scalar" && -z "$METRIC_CMD" ]]; then
  echo "ERROR: --metric is required for scalar eval mode."
  exit 1
fi

if [[ "$EVAL_MODE" == "binary" && -z "$EVALS_FILE" ]]; then
  echo "ERROR: --evals is required for binary eval mode."
  exit 1
fi

if [[ "$EVAL_MODE" == "binary" && ! -f "$EVALS_FILE" ]]; then
  echo "ERROR: Evals file not found: $EVALS_FILE"
  exit 1
fi

if [[ ! -f "$MUTABLE_FILE" ]]; then
  echo "ERROR: Mutable file not found: $MUTABLE_FILE"
  exit 1
fi

# Ensure we're inside a git repo
REPO_ROOT=$(git -C "$(dirname "$MUTABLE_FILE")" rev-parse --show-toplevel 2>/dev/null || true)
if [[ -z "$REPO_ROOT" ]]; then
  echo "ERROR: $MUTABLE_FILE is not inside a git repository."
  echo "Run: git init && git add . && git commit -m 'initial' in the target directory."
  exit 1
fi

# ── Setup results dir ─────────────────────────────────────────────────────────
RESULTS_DIR="$SKILL_DIR/results/$SESSION_NAME"
mkdir -p "$RESULTS_DIR"
TSV_FILE="$RESULTS_DIR/results.tsv"
REPORT_FILE="$RESULTS_DIR/report.md"
BEST_FILE="$RESULTS_DIR/best.md"
HYPOTHESIS_LOG="$RESULTS_DIR/hypothesis_log.jsonl"

# Write TSV header
echo -e "iteration\tmetric_before\tmetric_after\tkept\tchange_desc" > "$TSV_FILE"

# Initialize hypothesis log
touch "$HYPOTHESIS_LOG"

# ── Helpers ───────────────────────────────────────────────────────────────────
log() { echo "[auto-optimizer] $*"; }

run_scalar_metric() {
  local result
  result=$(eval "$METRIC_CMD" 2>/dev/null | grep -oE '[0-9]+\.?[0-9]*([eE][+-]?[0-9]+)?' | tail -1)
  echo "${result:-0}"
}

is_improvement() {
  local before="$1" after="$2"
  if [[ "$GOAL" == "minimize" ]]; then
    echo "$after < $before" | bc -l
  else
    echo "$after > $before" | bc -l
  fi
}

# Log a hypothesis to the JSONL file
log_hypothesis() {
  local iter="$1" hypothesis="$2" change_desc="$3" metric_before="$4" metric_after="$5" kept="$6" reason="$7"
  local entry
  entry=$(jq -n \
    --argjson iter "$iter" \
    --arg hypothesis "$hypothesis" \
    --arg change_desc "$change_desc" \
    --arg metric_before "$metric_before" \
    --arg metric_after "$metric_after" \
    --argjson kept "$kept" \
    --arg reason "$reason" \
    '{iter: $iter, hypothesis: $hypothesis, change_desc: $change_desc, metric_before: $metric_before, metric_after: $metric_after, kept: $kept, reason: $reason}' 2>/dev/null || \
    echo "{\"iter\":$iter,\"hypothesis\":\"$hypothesis\",\"change_desc\":\"$change_desc\",\"metric_before\":\"$metric_before\",\"metric_after\":\"$metric_after\",\"kept\":$kept,\"reason\":\"$reason\"}")
  echo "$entry" >> "$HYPOTHESIS_LOG"
}

# Get last N entries from hypothesis log as context string
get_hypothesis_context() {
  local n="${1:-5}"
  if [[ ! -s "$HYPOTHESIS_LOG" ]]; then
    echo "(No previous iterations logged yet.)"
    return
  fi
  local count
  count=$(wc -l < "$HYPOTHESIS_LOG")
  if [[ "$count" -eq 0 ]]; then
    echo "(No previous iterations logged yet.)"
    return
  fi
  echo "## Previous Hypotheses (last $n iterations — do NOT retry failed approaches):"
  echo ""
  tail -n "$n" "$HYPOTHESIS_LOG" | while IFS= read -r line; do
    local iter hypothesis kept reason metric_before metric_after
    iter=$(echo "$line" | grep -o '"iter":[0-9]*' | grep -o '[0-9]*' || echo "?")
    hypothesis=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('hypothesis',''))" 2>/dev/null || echo "")
    change_desc=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('change_desc',''))" 2>/dev/null || echo "")
    kept=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print('KEPT' if d.get('kept') else 'REVERTED')" 2>/dev/null || echo "?")
    metric_before=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('metric_before','?'))" 2>/dev/null || echo "?")
    metric_after=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('metric_after','?'))" 2>/dev/null || echo "?")
    reason=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('reason',''))" 2>/dev/null || echo "")
    echo "- Iter $iter [$kept] $metric_before → $metric_after: $change_desc"
    [[ -n "$reason" ]] && echo "  Reason: $reason"
  done
}

# Run binary eval: generate N outputs and score against evals.md
run_binary_eval() {
  local file="$1" evals="$2" batch="$3" iter="$4"
  local hypothesis_context="$5"
  local pass_count=0
  local total_checks=0
  local eval_criteria
  eval_criteria=$(cat "$evals")
  local num_criteria
  num_criteria=$(grep -c '^\s*[0-9]\+\.' "$evals" 2>/dev/null || echo "5")

  log "Running binary eval: $batch outputs × $num_criteria criteria = $((batch * num_criteria)) total checks"

  for ((b=1; b<=batch; b++)); do
    # Generate one output
    local gen_prompt
    gen_prompt=$(cat <<EOF
$(cat "$file")

---
Generate one high-quality output based on the above. Output ONLY the generated content, no preamble.
EOF
)
    local output
    if command -v claude &>/dev/null; then
      output=$(echo "$gen_prompt" | claude --print --no-conversation 2>/dev/null || echo "")
    else
      output="[generation failed]"
    fi

    if [[ -z "$output" ]]; then
      log "WARN: generation $b returned empty. Skipping."
      continue
    fi

    # Score against each eval criterion
    local eval_prompt
    eval_prompt=$(cat <<EOF
You are an evaluator. Score the following output against each criterion.

## Output to Evaluate:
$output

## Eval Criteria:
$eval_criteria

For each numbered criterion, respond with exactly "PASS" or "FAIL" on a new line.
Output ONLY the PASS/FAIL results, one per line, in order.
EOF
)
    local scores
    if command -v claude &>/dev/null; then
      scores=$(echo "$eval_prompt" | claude --print --no-conversation 2>/dev/null || echo "")
    else
      scores=""
    fi

    local passes
    passes=$(echo "$scores" | grep -c "^PASS$" || echo "0")
    local fails
    fails=$(echo "$scores" | grep -c "^FAIL$" || echo "0")
    local this_total=$((passes + fails))

    pass_count=$((pass_count + passes))
    total_checks=$((total_checks + this_total))
    log "  Sample $b: $passes/$this_total passed"
  done

  if [[ "$total_checks" -eq 0 ]]; then
    echo "0"
  else
    # Return as percentage 0-100
    echo "scale=2; $pass_count * 100 / $total_checks" | bc -l
  fi
}

call_agent() {
  local file="$1" program="$2" iteration="$3" hypothesis_context="$4"
  local prompt

  prompt=$(cat <<EOF
$(cat "$program")

---
$hypothesis_context

---
## Current File: $(basename "$file")
\`\`\`
$(cat "$file")
\`\`\`

## Your Task
You are iteration $iteration of an autonomous optimization loop.
Propose ONE targeted change to the file above that you hypothesize will improve the metric.
Study the hypothesis history above carefully — do NOT retry approaches that already failed.

Output ONLY the following format (nothing else):
HYPOTHESIS: <one sentence: what you believe and why>
CHANGE_DESC: <one sentence describing the specific change you're making>
FILE_CONTENT:
<complete new file content with your change applied>
EOF
)

  if command -v claude &>/dev/null; then
    echo "$prompt" | claude --print --no-conversation 2>/dev/null || echo ""
  else
    local tmp_prompt="$RESULTS_DIR/prompt_iter${iteration}.txt"
    echo "$prompt" > "$tmp_prompt"
    log "claude CLI not found. Falling back to openclaw claude-code skill..."
    if [[ -f "$SKILL_DIR/../claude-code/claude-code.sh" ]]; then
      bash "$SKILL_DIR/../claude-code/claude-code.sh" "$(cat "$tmp_prompt")" "autoopt-$SESSION_NAME" 2>/dev/null || echo ""
    else
      log "ERROR: No claude CLI or claude-code skill found. Cannot run agent."
      echo ""
    fi
  fi
}

parse_agent_output() {
  local output="$1"
  local part="$2"  # "hypothesis", "desc", or "content"

  if [[ "$part" == "hypothesis" ]]; then
    echo "$output" | grep -m1 "^HYPOTHESIS:" | sed 's/^HYPOTHESIS: *//' | head -c 300
  elif [[ "$part" == "desc" ]]; then
    echo "$output" | grep -m1 "^CHANGE_DESC:" | sed 's/^CHANGE_DESC: *//' | head -c 200
  elif [[ "$part" == "content" ]]; then
    echo "$output" | awk '/^FILE_CONTENT:/{found=1; next} found{print}'
  fi
}

# ── Determine program.md ──────────────────────────────────────────────────────
if [[ -z "$PROGRAM_FILE" ]]; then
  PROGRAM_FILE="$SKILL_DIR/program.md.template"
  # Fall back to autoresearch-loop template if not found
  if [[ ! -f "$PROGRAM_FILE" ]]; then
    PROGRAM_FILE="$SKILL_DIR/../autoresearch-loop/program.md.template"
  fi
fi

if [[ ! -f "$PROGRAM_FILE" ]]; then
  echo "ERROR: program file not found: $PROGRAM_FILE"
  exit 1
fi

# ── Banner ────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              Auto-Optimizer — OpenClaw                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
log "Session:     $SESSION_NAME"
log "File:        $MUTABLE_FILE"
log "Eval mode:   $EVAL_MODE"
if [[ "$EVAL_MODE" == "scalar" ]]; then
  log "Metric:      $METRIC_CMD"
  log "Goal:        $GOAL"
else
  log "Evals:       $EVALS_FILE"
  log "Batch size:  $BATCH_SIZE"
fi
log "Budget:      $BUDGET iterations"
log "Results dir: $RESULTS_DIR"
echo ""

# ── Baseline ──────────────────────────────────────────────────────────────────
log "Running baseline measurement..."
if [[ "$EVAL_MODE" == "scalar" ]]; then
  BASELINE=$(run_scalar_metric)
else
  BASELINE=$(run_binary_eval "$MUTABLE_FILE" "$EVALS_FILE" "$BATCH_SIZE" "0" "")
fi
log "Baseline: $BASELINE"

# Save best version
cp "$MUTABLE_FILE" "$BEST_FILE"
BEST_METRIC="$BASELINE"
BEST_ITERATION=0

# Ensure current state is committed
git -C "$REPO_ROOT" add "$MUTABLE_FILE" 2>/dev/null || true
git -C "$REPO_ROOT" diff --cached --quiet "$MUTABLE_FILE" 2>/dev/null || \
  git -C "$REPO_ROOT" commit -m "auto-optimizer[$SESSION_NAME]: baseline" -- "$MUTABLE_FILE" 2>/dev/null || true

# ── Main Loop ─────────────────────────────────────────────────────────────────
KEPT=0
REVERTED=0
START_TIME=$(date +%s)

for ((ITER=1; ITER<=BUDGET; ITER++)); do
  echo ""
  log "━━━ Iteration $ITER / $BUDGET ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Get current metric
  if [[ "$EVAL_MODE" == "scalar" ]]; then
    METRIC_BEFORE=$(run_scalar_metric)
  else
    METRIC_BEFORE="$BEST_METRIC"  # In binary mode, use best known score as baseline
  fi
  log "Metric before: $METRIC_BEFORE"

  # Build hypothesis context from log
  HYPOTHESIS_CONTEXT=$(get_hypothesis_context 5)

  # Call agent
  log "Calling agent..."
  AGENT_OUTPUT=$(call_agent "$MUTABLE_FILE" "$PROGRAM_FILE" "$ITER" "$HYPOTHESIS_CONTEXT")

  if [[ -z "$AGENT_OUTPUT" ]]; then
    log "WARN: Agent returned empty output. Skipping iteration."
    echo -e "$ITER\t$METRIC_BEFORE\t$METRIC_BEFORE\tskipped\t(agent error)" >> "$TSV_FILE"
    continue
  fi

  # Parse output
  HYPOTHESIS=$(parse_agent_output "$AGENT_OUTPUT" "hypothesis")
  CHANGE_DESC=$(parse_agent_output "$AGENT_OUTPUT" "desc")
  NEW_CONTENT=$(parse_agent_output "$AGENT_OUTPUT" "content")

  if [[ -z "$NEW_CONTENT" ]]; then
    log "WARN: Could not parse file content from agent output. Skipping."
    echo -e "$ITER\t$METRIC_BEFORE\t$METRIC_BEFORE\tskipped\t(parse error)" >> "$TSV_FILE"
    continue
  fi

  log "Hypothesis: $HYPOTHESIS"
  log "Change: $CHANGE_DESC"

  # Apply change
  echo "$NEW_CONTENT" > "$MUTABLE_FILE"

  # Run metric
  if [[ "$EVAL_MODE" == "scalar" ]]; then
    METRIC_AFTER=$(run_scalar_metric)
  else
    METRIC_AFTER=$(run_binary_eval "$MUTABLE_FILE" "$EVALS_FILE" "$BATCH_SIZE" "$ITER" "$HYPOTHESIS_CONTEXT")
  fi
  log "Metric after:  $METRIC_AFTER"

  # Evaluate
  IMPROVED=$(is_improvement "$METRIC_BEFORE" "$METRIC_AFTER" 2>/dev/null || echo "0")

  if [[ "$IMPROVED" == "1" ]]; then
    log "✅ KEPT — improvement: $METRIC_BEFORE → $METRIC_AFTER"
    git -C "$REPO_ROOT" add "$MUTABLE_FILE" 2>/dev/null || true
    git -C "$REPO_ROOT" commit -m "auto-optimizer[$SESSION_NAME] iter=$ITER: $CHANGE_DESC" -- "$MUTABLE_FILE" 2>/dev/null || true
    echo -e "$ITER\t$METRIC_BEFORE\t$METRIC_AFTER\tkept\t$CHANGE_DESC" >> "$TSV_FILE"
    KEPT=$((KEPT+1))

    # Log to hypothesis memory
    log_hypothesis "$ITER" "$HYPOTHESIS" "$CHANGE_DESC" "$METRIC_BEFORE" "$METRIC_AFTER" "true" "Improvement confirmed"

    # Track best
    IS_BEST=$(is_improvement "$BEST_METRIC" "$METRIC_AFTER" 2>/dev/null || echo "0")
    if [[ "$IS_BEST" == "1" ]]; then
      cp "$MUTABLE_FILE" "$BEST_FILE"
      BEST_METRIC="$METRIC_AFTER"
      BEST_ITERATION="$ITER"
    fi
  else
    log "❌ REVERTED — no improvement: $METRIC_BEFORE → $METRIC_AFTER"
    git -C "$REPO_ROOT" checkout -- "$MUTABLE_FILE" 2>/dev/null || true
    echo -e "$ITER\t$METRIC_BEFORE\t$METRIC_AFTER\treverted\t$CHANGE_DESC" >> "$TSV_FILE"
    REVERTED=$((REVERTED+1))

    # Log to hypothesis memory (with reason for failure)
    log_hypothesis "$ITER" "$HYPOTHESIS" "$CHANGE_DESC" "$METRIC_BEFORE" "$METRIC_AFTER" "false" "No metric improvement - this direction did not help"
  fi
done

# ── Final Report ──────────────────────────────────────────────────────────────
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
TOTAL_ITERS=$((KEPT + REVERTED))

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  Auto-Optimizer Complete                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
log "Iterations run: $TOTAL_ITERS (budget: $BUDGET)"
log "Kept:           $KEPT"
log "Reverted:       $REVERTED"
log "Baseline:       $BASELINE"
log "Best metric:    $BEST_METRIC (iteration $BEST_ITERATION)"
log "Elapsed:        ${ELAPSED}s"
log "Results:        $TSV_FILE"
log "Hypothesis log: $HYPOTHESIS_LOG"
log "Best file:      $BEST_FILE"

# Write report
cat > "$REPORT_FILE" <<EOF
# Auto-Optimizer Report — $SESSION_NAME
Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

## Summary
| | |
|---|---|
| Session | $SESSION_NAME |
| Mutable File | $MUTABLE_FILE |
| Eval Mode | $EVAL_MODE |
| Budget | $BUDGET iterations |
| Iterations Run | $TOTAL_ITERS |
| Kept | $KEPT |
| Reverted | $REVERTED |
| Elapsed | ${ELAPSED}s |

## Results
| Metric | Value |
|--------|-------|
| Baseline | $BASELINE |
| Best | $BEST_METRIC |
| Best Iteration | $BEST_ITERATION |

## Experiment Log
$(cat "$TSV_FILE" | column -t -s $'\t')

## Hypothesis Memory
$(cat "$HYPOTHESIS_LOG" | head -20)

## Best Version
Saved to: \`$BEST_FILE\`
EOF

echo ""
log "Full report: $REPORT_FILE"
echo ""
cat "$REPORT_FILE"
