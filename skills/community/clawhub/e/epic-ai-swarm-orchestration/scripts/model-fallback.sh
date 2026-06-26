#!/usr/bin/env bash
# model-fallback.sh — Pick the next available model for a role after a failure
#
# Usage: model-fallback.sh <role> <failed-agent> <failed-model>
# Output: agent|model|nonInteractiveCmd   (pipe-separated)
# Exit 0 = found fallback, Exit 1 = no fallback available
#
# Fallback priority per role:
#   architect:  codex → gemini-2.5-pro → deepseek-v4-pro-max
#   builder:    deepseek-v4-pro-max → codex → gemini-2.5-pro
#   reviewer:   deepseek-v4-pro-max → gemini-2.5-pro → codex
#   integrator: codex → gemini-2.5-pro → deepseek-v4-pro-max

set -euo pipefail

ROLE="${1:?Usage: model-fallback.sh <role> <failed-agent> <failed-model>}"
FAILED_AGENT="${2:?Missing failed-agent}"
FAILED_MODEL="${3:?Missing failed-model}"

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"

# All candidate models in priority order per role
# Each entry: agent:model
declare -A FALLBACK_CHAINS
FALLBACK_CHAINS[architect]="codex:gpt-5.5 gemini:gemini-2.5-pro deepseek:deepseek-v4-pro-max codex:gpt-5.3-codex"
FALLBACK_CHAINS[builder]="deepseek:deepseek-v4-pro-max codex:gpt-5.5 gemini:gemini-2.5-pro codex:gpt-5.3-codex"
FALLBACK_CHAINS[reviewer]="deepseek:deepseek-v4-pro-max gemini:gemini-2.5-pro codex:gpt-5.5 codex:gpt-5.3-codex"
FALLBACK_CHAINS[integrator]="codex:gpt-5.5 gemini:gemini-2.5-pro deepseek:deepseek-v4-pro-max codex:gpt-5.3-codex"

CHAIN="${FALLBACK_CHAINS[$ROLE]:-${FALLBACK_CHAINS[builder]}}"

build_cmd() {
  local agent="$1" model="$2"
  case "$agent" in
    # Use `codex exec` as the subcommand; `codex --full-auto` alone fails in
    # tmux with "stdout is not a terminal". exec is the non-interactive entry.
    codex)  echo "codex exec --model $model --full-auto" ;;
    gemini) echo "gemini -m $model -p" ;;
    deepseek) echo "deepseek -m $model -y -p" ;;
  esac
}

echo "[model-fallback] Role=$ROLE, failed=$FAILED_AGENT/$FAILED_MODEL" >&2
echo "[model-fallback] Testing fallback chain..." >&2

for candidate in $CHAIN; do
  IFS=':' read -r agent model <<< "$candidate"

  # Skip the one that just failed
  if [[ "$agent" == "$FAILED_AGENT" && "$model" == "$FAILED_MODEL" ]]; then
    echo "[model-fallback]   skip $agent/$model (just failed)" >&2
    continue
  fi

  # Quick health check (15s timeout — faster than full assess)
  echo "[model-fallback]   testing $agent/$model ..." >&2
  if "$SWARM_DIR/try-model.sh" "$agent" "$model" 2>/dev/null; then
    CMD=$(build_cmd "$agent" "$model")
    echo "[model-fallback] ✅ Fallback found: $agent/$model" >&2
    echo "${agent}|${model}|${CMD}"
    exit 0
  else
    echo "[model-fallback]   ❌ $agent/$model also unavailable" >&2
  fi
done

echo "[model-fallback] ❌ No fallback available for $ROLE" >&2
exit 1
