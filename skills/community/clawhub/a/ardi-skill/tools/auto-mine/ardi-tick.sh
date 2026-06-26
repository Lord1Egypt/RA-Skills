#!/usr/bin/env bash
# ardi-tick.sh — Ardi mining tick dispatcher.
#
# Called every 60-90s by systemd timer (see systemd/ardi-mine.timer).
# Workflow:
#   1. Cheap precheck: is there anything actionable on chain or in local
#      pending state? If not, exit 0 — saves the cost of spawning an
#      LLM agent for an obvious no-op tick.
#   2. Pick the configured runtime (claude / hermes / openclaw-scripted).
#   3. Spawn the subagent with our shared prompt.
#   4. Subagent runs one mining tick (commit / reveal / inscribe drive)
#      and exits.
#
# Idempotent: skill-side state dedups commits + reveals automatically,
# so multiple ticks per second wouldn't double-spend. The precheck just
# saves tokens.

set -euo pipefail

# ── Config ──────────────────────────────────────────────────────────
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="${ARDI_AGENT_RUNTIME:-claude}"   # claude | hermes | openclaw
PROMPT="$HERE/prompt/ardi-mine-tick.md"
ARDI_AGENT="${ARDI_AGENT_BIN:-ardi-agent}"
SERVER="${ARDI_SERVER:-}"

ts() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
log() { echo "[$(ts)] tick: $*"; }

# ── Sanity checks ───────────────────────────────────────────────────
command -v "$ARDI_AGENT" >/dev/null || {
  log "FATAL: $ARDI_AGENT not on PATH; install via 'cargo install --path ...' or download release"
  exit 64
}
[[ -r "$PROMPT" ]] || {
  log "FATAL: prompt missing at $PROMPT"
  exit 65
}

RUNTIME_SH="$HERE/runtime/${RUNTIME}.sh"
[[ -x "$RUNTIME_SH" ]] || {
  log "FATAL: unknown runtime '$RUNTIME' (expected: claude | hermes | openclaw-scripted)"
  exit 66
}

# ── Cheap precheck: is there anything to do? ────────────────────────
# Goal: only spawn the LLM agent when there's signal.
# Signal sources (any one is enough):
#   (a) coord-rs reports an open epoch in commit window
#   (b) local commits.json has any pending entry not in terminal state
SERVER_ARG=()
[[ -n "$SERVER" ]] && SERVER_ARG=(--server "$SERVER")

# Use --quiet/--json-only output if available; ardi-agent always prints
# JSON so we can grep tolerantly for either condition.
need_to_run="no"
reason=""

# (a) check current epoch
if ctx="$($ARDI_AGENT "${SERVER_ARG[@]}" context 2>/dev/null)"; then
  # has epoch + commit_deadline > now
  has_open_epoch="$(echo "$ctx" | grep -E '"commit_deadline"\s*:' | head -1 || true)"
  if [[ -n "$has_open_epoch" ]]; then
    deadline="$(echo "$ctx" | sed -nE 's/.*"commit_deadline"\s*:\s*([0-9]+).*/\1/p' | head -1)"
    now="$(date +%s)"
    if [[ -n "$deadline" && "$deadline" -gt "$now" ]]; then
      need_to_run="yes"
      reason="commit window open (closes in $((deadline - now))s)"
    fi
  fi
fi

# (b) check local pending commits — drives reveal / inscribe even when
#     no current commit window
if [[ "$need_to_run" == "no" ]]; then
  if commits="$($ARDI_AGENT "${SERVER_ARG[@]}" commits 2>/dev/null)"; then
    pending="$(echo "$commits" | grep -cE '"status"\s*:\s*"(committed|revealed|won)"' || true)"
    if [[ "${pending:-0}" -gt 0 ]]; then
      need_to_run="yes"
      reason="$pending pending entries to drive forward"
    fi
  fi
fi

if [[ "$need_to_run" == "no" ]]; then
  log "no work — skipping (no open commit window, no pending state)"
  exit 0
fi

# ── Spawn subagent ──────────────────────────────────────────────────
log "spawning $RUNTIME — $reason"
exec "$RUNTIME_SH" "$PROMPT"
