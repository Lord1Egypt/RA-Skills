#!/bin/bash
# foreman fleet-check — pipeline health check before a batch dispatch.
# Any FAIL exits non-zero. Optional channels only WARN.
fail=0
ok(){ printf 'PASS  %s\n' "$1"; }
bad(){ printf 'FAIL  %s\n      fix: %s\n' "$1" "$2"; fail=1; }
warn(){ printf 'WARN  %s\n' "$1"; }
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Builder line: handoff (public CLI, this is the one foreman dispatches through)
command -v handoff >/dev/null 2>&1 && ok "handoff CLI" \
  || bad "handoff not installed" "uv tool install handoff-cli==4.0.2 && handoff init"
[ -f "$HOME/.handoff/config.yaml" ] && ok "handoff config" \
  || bad "handoff has no config" "edit ~/.handoff/config.yaml and configure your backends"

# 1a. The dispatch example depends on both helper scripts. Without worktree-setup.sh, dispatch falls back to
# running workers in your own checkout — the path that already caused an incident.
for s in backend-health.sh worktree-setup.sh; do
  if [ -f "$SKILL_DIR/$s" ]; then ok "$s present"
  else bad "$s missing next to fleet-check.sh" "reinstall the skill — dispatch.md §3 calls it directly"; fi
done

# 1b. Which backends are usable right now (same probe dispatch uses; failures here are not fatal on their own).
if python3 -c '' 2>/dev/null; then
  if picked=$(bash "$SKILL_DIR/backend-health.sh" pick 2>/dev/null); then
    ok "worker pool has a usable backend: $picked (FOREMAN_POOL=${FOREMAN_POOL:-deepseek})"
  else
    bad "no usable backend in FOREMAN_POOL=${FOREMAN_POOL:-deepseek}" "run: bash $SKILL_DIR/backend-health.sh status — then fix the login/quota/config it names"
  fi
else
  bad "python3 not found" "backend-health.sh needs python3 for its state table"
fi

# 1c. Two claude-type backends sharing one CLAUDE_CONFIG_DIR: a subscription token can leak into an API-key
# backend, which then answers 401 "api key invalid" — the error points at the key, the cause is the shared login.
if command -v handoff >/dev/null 2>&1; then
  seen=""
  for be in ${FOREMAN_POOL:-deepseek}; do
    d=$(cd /tmp && handoff run --dry-run --backend "$be" --text hi 2>/dev/null | grep -oE 'CLAUDE_CONFIG_DIR=[^ ]*' | head -1)
    [ -n "$d" ] || continue
    other=$(printf '%s\n' "$seen" | awk -v d="$d" '$2==d {print $1; exit}')
    if [ -n "$other" ]; then
      warn "backends '$other' and '$be' share $d — if one uses a subscription login and the other an API key, give the API-key one its own CLAUDE_CONFIG_DIR in its env block"
    fi
    seen="$seen
$be $d"
  done
fi

# 2. QA line: a second-opinion CLI from another vendor, for escalation
if command -v codex >/dev/null 2>&1; then
  ok "codex CLI (for non-interactive calls remember --skip-git-repo-check and stdin from /dev/null)"
  # Ask the CLI about its own auth rather than stat-ing its credential file.
  if codex login status >/dev/null 2>&1; then
    ok "codex logged in"
  else
    warn "codex login state unconfirmed — if dispatch fails with 401, run: codex login"
  fi
else
  warn "codex CLI absent — escalation falls back to the main session (npm i -g @openai/codex)"
fi

# 3. Acceptance line: dynamic checker (optional; see verify.md section 1)
if [ -n "${FOREMAN_HARDENING_CMD:-}" ]; then
  ok "dynamic checker configured (FOREMAN_HARDENING_CMD)"
else
  warn "no FOREMAN_HARDENING_CMD — acceptance degrades to task-level verification only (correct for libraries/CLIs/backends)"
fi

# 4. Cursor agent (optional pool member)
command -v cursor-agent >/dev/null 2>&1 || command -v agent >/dev/null 2>&1 \
  && ok "cursor agent CLI" \
  || warn "cursor agent absent (optional pool member; see cursor.com for its installer)"

# 5. Container line: caged worker (optional). Checked against FOREMAN_DOCKER_CONTEXT when set, because some
# container runtimes switch Docker's default context when they start — the image may exist in a context
# that isn't the current default, and an unpinned check reports a false WARN.
dctx=(); [ -n "${FOREMAN_DOCKER_CONTEXT:-}" ] && dctx=(--context "$FOREMAN_DOCKER_CONTEXT")
if [ -z "${FOREMAN_WORKER_IMAGE:-}" ]; then
  warn "caged worker not configured (build the pinned image from dispatch.md §3, then set FOREMAN_WORKER_IMAGE to its sha256 id)"
elif docker ${dctx[@]+"${dctx[@]}"} image inspect "$FOREMAN_WORKER_IMAGE" >/dev/null 2>&1 && docker ${dctx[@]+"${dctx[@]}"} info >/dev/null 2>&1; then
  ok "caged worker (pinned image present + live daemon${FOREMAN_DOCKER_CONTEXT:+, context $FOREMAN_DOCKER_CONTEXT})"
else
  warn "caged worker unavailable: FOREMAN_WORKER_IMAGE not found or daemon down (start your container runtime; rebuild from dispatch.md §3 if the image is gone)"
fi

# 6. Environment contamination (hard rule: a worker's key must never leak into your shell)
# For the main session, a globally exported ANTHROPIC_API_KEY outranks a subscription login — the foreman silently
# switches from subscription quota to pay-as-you-go billing. (handoff clears it for workers; this is about you.)
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  bad "ANTHROPIC_API_KEY is exported in this shell (value not printed)" \
      "remove it from your shell rc — it moves the main session off your subscription onto metered billing, without any notice"
else
  ok "no ANTHROPIC_API_KEY in the shell"
fi
case "${ANTHROPIC_BASE_URL:-}" in
  ""|https://api.anthropic.com|https://api.anthropic.com/) ok "no ANTHROPIC_BASE_URL leak" ;;
  *) bad "ANTHROPIC_BASE_URL is set to a non-default value (not printed here — it can carry a token)" \
        "remove it from your shell rc — it silently reroutes every agent session on this machine to another backend" ;;
esac

exit $fail
