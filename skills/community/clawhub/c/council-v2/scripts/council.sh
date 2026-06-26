#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROLE_PROMPTS="$SKILL_DIR/references/role-prompts.md"
SCHEMA_REF="$SKILL_DIR/references/schema.md"
SYNTH="$SKILL_DIR/scripts/synthesize.py"

TIER="standard"
FORMAT="text"
OPTIONS=""
INPUT_FILE=""
MODEL_OPUS="opus"
MODEL_GPT="gpt-5.4"
MODEL_GROK="grok4"
MODEL_DEEPSEEK="deepseek"
MODEL_GEMINI="gemini"

usage() {
  cat <<EOF
Usage:
  bash scripts/council.sh review <type> [file] [--tier standard|full] [--options "A,B,C"] [--format text|json]
  bash scripts/council.sh synthesize <reviewer-json...>

Examples:
  bash scripts/council.sh review code src/auth.py
  bash scripts/council.sh review architecture design.md --tier full
  cat plan.md | bash scripts/council.sh review plan --tier full
  bash scripts/council.sh synthesize out/*.json
EOF
}

[[ $# -ge 1 ]] || { usage; exit 1; }
CMD="$1"; shift

if [[ "$CMD" == "synthesize" ]]; then
  python3 "$SYNTH" "$@"
  exit $?
fi

[[ "$CMD" == "review" ]] || { usage; exit 1; }
[[ $# -ge 1 ]] || { usage; exit 1; }
TYPE="$1"; shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tier) TIER="$2"; shift 2 ;;
    --options) OPTIONS="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --opus) MODEL_OPUS="$2"; shift 2 ;;
    --gpt) MODEL_GPT="$2"; shift 2 ;;
    --grok) MODEL_GROK="$2"; shift 2 ;;
    --deepseek) MODEL_DEEPSEEK="$2"; shift 2 ;;
    --gemini) MODEL_GEMINI="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    --*) echo "unknown option: $1" >&2; exit 1 ;;
    *) INPUT_FILE="$1"; shift ;;
  esac
done

if [[ -n "$INPUT_FILE" ]]; then
  CONTENT="$(cat "$INPUT_FILE")"
elif [[ ! -t 0 ]]; then
  CONTENT="$(cat)"
else
  CONTENT=""
fi

if [[ "$TIER" == "standard" ]]; then
  REVIEWERS=$(cat <<EOF
- role: Architecture Synthesizer
  model: $MODEL_OPUS
- role: Adversarial Critic
  model: $MODEL_GPT
- role: Security & Risk
  model: $MODEL_GROK
EOF
)
else
  REVIEWERS=$(cat <<EOF
- role: Architecture Synthesizer
  model: $MODEL_OPUS
- role: Adversarial Critic
  model: $MODEL_GPT
- role: Security & Risk
  model: $MODEL_GROK
- role: First Principles
  model: $MODEL_DEEPSEEK
- role: Structural Verifier
  model: $MODEL_GEMINI
EOF
)
fi

PROMPT=$(cat <<EOF
# Council v2 Orchestration Plan

Review type: $TYPE
Tier: $TIER
Role prompts reference: $ROLE_PROMPTS
Schema reference: $SCHEMA_REF

Dispatch these reviewers with sessions_spawn in parallel:
$REVIEWERS

Instructions:
1. Give each reviewer the content under review plus its role prompt from role-prompts.md.
2. Require JSON-only output matching schema.md.
3. Save each review as a JSON file.
4. Run: python3 "$SYNTH" <all reviewer json files>
5. On Full Council, present raw reviewer outputs along with synthesis.
6. Synthesizer narrates result but does not override vote count.

Decision options: ${OPTIONS:-N/A}

Content under review:
---
$CONTENT
---
EOF
)

if [[ "$FORMAT" == "json" ]]; then
  python3 - <<PY
import json
print(json.dumps({"type": "$TYPE", "tier": "$TIER", "options": "$OPTIONS", "orchestration_prompt": '''$PROMPT'''}, indent=2))
PY
else
  printf '%s\n' "$PROMPT"
fi
