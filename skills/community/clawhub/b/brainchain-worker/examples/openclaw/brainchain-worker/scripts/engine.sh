#!/bin/sh
# Does one BrainChain task: the brief arrives on stdin, the result leaves on stdout.
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
state=${OPENCLAW_WORKER_STATE:-$HOME/.openclaw-brainchain-worker}
mkdir -p "$state"
work=$(mktemp -d "${TMPDIR:-/tmp}/brainchain-task.XXXXXX")
# openclaw.json names this turn's container and workspace from these, so its end removes them and nothing else.
OPENCLAW_WORKER_RUN=${work##*.}
OPENCLAW_WORKER_SANDBOXES=$state/sandboxes/$OPENCLAW_WORKER_RUN
export OPENCLAW_WORKER_RUN OPENCLAW_WORKER_SANDBOXES
finish() {
  # A brief can leave processes running in the container, which end with it.
  ids=$(docker ps -aq --filter label=openclaw.sandbox=1 --filter "name=openclaw-bc-$OPENCLAW_WORKER_RUN-" 2>/dev/null) || ids=
  [ -z "$ids" ] || docker rm -f $ids >/dev/null 2>&1 || :
  rm -rf "$work" "$OPENCLAW_WORKER_SANDBOXES" 2>/dev/null || :
}
trap finish EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
openclaw agent exec --message-file - \
  --config "$here/openclaw.json" --state-dir "$state" \
  --model "${OPENCLAW_WORKER_MODEL:-openrouter/deepseek/deepseek-v4.1-flash}" \
  --cwd "$work" --timeout "${OPENCLAW_WORKER_TIMEOUT:-1080}" 2>>"$state/engine.log"
