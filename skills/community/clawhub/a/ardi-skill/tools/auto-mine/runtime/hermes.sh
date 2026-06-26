#!/usr/bin/env bash
# runtime/hermes.sh — invoke Hermes (NousResearch) with the ardi tick prompt.
#
# Hermes auto-loads any skill placed under ~/.hermes/skills/ — so as long
# as the user has installed ardi-skill there (the install.sh script links
# it), the agent can call `ardi-agent` directly via its terminal toolset.
#
# Requires:
#   - hermes binary on PATH
#   - ardi skill linked at ~/.hermes/skills/ardi/SKILL.md
#   - LLM API key configured in hermes config (provider-agnostic)

set -euo pipefail

PROMPT_FILE="${1:?usage: hermes.sh <prompt-file>}"
[[ -r "$PROMPT_FILE" ]] || { echo "prompt not readable: $PROMPT_FILE" >&2; exit 2; }

command -v hermes >/dev/null || { echo "hermes not on PATH" >&2; exit 3; }

# `chat -Q -q`: programmatic mode + one-shot query
# -s ardi: preload the ardi skill (auto-discovered from ~/.hermes/skills/ardi)
# --toolsets terminal,skills: terminal so it can run ardi-agent, skills so
#   it can call sub-skills if any. No web/file toolsets — they're not needed
#   and reduce attack surface for a long-running daemon.
PROMPT="$(cat "$PROMPT_FILE")"
exec hermes chat -Q -q "$PROMPT" \
  -s ardi \
  --toolsets terminal,skills
