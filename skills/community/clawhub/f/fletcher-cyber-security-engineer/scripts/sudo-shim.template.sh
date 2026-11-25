#!/usr/bin/env bash
# sudo shim for OpenClaw, installed as ~/.openclaw/bin/sudo by
# install-openclaw-runtime-hook.sh. Do not edit the installed copy: reinstall instead.
#
# Every sudo call that would run a command is handed to guarded_privileged_exec.py,
# which checks policy, asks for approval at the terminal and records the action.
#
# The three paths below are fixed when the shim is installed. They are deliberately
# not read from the environment, so a caller cannot point the shim at a different
# sudo, interpreter or guard.
set -euo pipefail

REAL_SUDO=@REAL_SUDO@
PYTHON3=@PYTHON3@
SKILL_DIR=@SKILL_DIR@

# With no arguments sudo only prints its usage.
if [[ $# -eq 0 ]]; then
  exec "${REAL_SUDO}"
fi

# A single flag that asks sudo about itself, or drops cached credentials, runs
# nothing. The same flag followed by anything else (for example "sudo -k rm ...")
# does run a command, so it is not passed through.
if [[ $# -eq 1 ]]; then
  case "$1" in
    -h|--help|-V|--version|-k|-K)
      exec "${REAL_SUDO}" "$1"
      ;;
  esac
fi

REASON="${OPENCLAW_PRIV_REASON:-OpenClaw requested privileged execution}"
# The reason is only shown and logged. Keep plain characters and cap the length.
REASON="$(printf '%s' "${REASON}" | tr -cd '[:alnum:] .,:_/@=+-' | cut -c1-200)"

exec "${PYTHON3}" "${SKILL_DIR}/scripts/guarded_privileged_exec.py" \
  --reason "${REASON}" \
  --use-sudo \
  -- "$@"
