#!/bin/bash
# foreman caged worker: bash foreman-cworker.sh <absolute-worktree-path> <prompt-file> [model]
#
# Blast radius = the mounted worktree + the container filesystem. The host $HOME, your
# other repos, and your primary agent login are all invisible to it, which is what makes
# --dangerously-skip-permissions acceptable here and nowhere else. That promise only holds if
# what gets mounted really is one task worktree, so this script checks it before starting anything:
#   * the worktree must resolve (after following symlinks) to a direct child of FOREMAN_WORKTREE_ROOT
#     (default ~/foreman-worktrees) — never $HOME, /, the root itself, or a symlink leading elsewhere;
#   * it must be a linked worktree that git has registered, not the main checkout or a stray directory;
#   * the prompt must be a regular file (not a symlink) inside FOREMAN_PROMPT_ROOT (default ~/.handoff/tasks).
#
# Credential boundary — what happens to DEEPSEEK_API_KEY:
#   * Read from your environment at call time. This script never writes it to disk,
#     never logs it, and never bakes it into an image. Keep it in a mode-600 file you
#     source for this call rather than a global shell export: a global export is readable
#     by every terminal and agent session, and some agent CLIs copy exported variables into
#     their own shell snapshots.
#   * Handed to the container as that worker's own API credential, so it is exposed
#     only to the process running inside the cage. This script never copies it into
#     the mounted worktree, and it is gone when the container exits (--rm).
#   * The worker is *configured* to call the ANTHROPIC_BASE_URL set below (change that line to
#     point at a different backend). That is configuration, not enforcement: this script does
#     not restrict the container's network, so code running inside it — including anything a
#     repository file talks the worker into — could reach other hosts and use the key there.
#     Treat the key as exposed to whatever runs in the cage: give this worker its own key with
#     the smallest spending limit you can, never a key that anything else depends on, and rotate it.
#     If you need a hard boundary, run the container on a network whose only exit is an
#     allowlisting proxy for that one host — this skill does not set that up for you.
#
# Supply chain: FOREMAN_WORKER_IMAGE must be an immutable image reference — the content-addressed
# image id (sha256:…) or name@sha256:… — never a tag like :latest, whose contents can change without
# anyone reviewing them. Build the image from the pinned Dockerfile in dispatch.md §3, then record its id.
#
# Git does not work inside the cage (the worktree's .git points at the host repository, which is not
# mounted), so the main session commits the delivery afterwards — see dispatch.md §3.
#
# FOREMAN_DOCKER_CONTEXT pins the Docker context the image was built in. Some container runtimes
# switch Docker's default context when they start; pinning it means this script neither depends on
# nor changes whatever your default happens to be.
set -euo pipefail
die(){ echo "foreman-cworker: $*" >&2; exit 1; }

WT_IN="${1:?usage: foreman-cworker.sh <absolute-worktree-path> <prompt-file> [model]}"
PROMPT_IN="${2:?usage: foreman-cworker.sh <absolute-worktree-path> <prompt-file> [model]}"
MODEL="${3:-deepseek-v4-flash}"

[ -n "${DEEPSEEK_API_KEY:-}" ] || die "DEEPSEEK_API_KEY is not set"

IMAGE="${FOREMAN_WORKER_IMAGE:-}"
[[ "$IMAGE" =~ ^(sha256:[0-9a-f]{64}|[^[:space:]@]+@sha256:[0-9a-f]{64})$ ]] \
  || die "FOREMAN_WORKER_IMAGE must be an immutable reference (sha256:<id> or name@sha256:<digest>), got '${IMAGE}'. After building: docker image inspect -f '{{.Id}}' foreman-worker"

# ── The worktree: a registered linked worktree, directly under the trusted root ──
ROOT_IN="${FOREMAN_WORKTREE_ROOT:-$HOME/foreman-worktrees}"
[ -d "$ROOT_IN" ] || die "worktree root does not exist: $ROOT_IN"
ROOT="$(cd "$ROOT_IN" && pwd -P)"
[ -d "$WT_IN" ] || die "worktree does not exist: $WT_IN"
WT="$(cd "$WT_IN" && pwd -P)"
[ "$(dirname "$WT")" = "$ROOT" ] || die "refusing to mount $WT_IN: it resolves to $WT, which is not a direct child of $ROOT"
for forbidden in / "$(cd "$HOME" && pwd -P)" "$ROOT"; do
  [ "$WT" != "$forbidden" ] || die "refusing to mount $WT"
done
[ -f "$WT/.git" ] || die "refusing to mount $WT: not a linked git worktree (no .git file) — create it with worktree-setup.sh"
COMMON="$(git -C "$WT" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)" \
  || die "refusing to mount $WT: git does not recognise it"
git --git-dir="$COMMON" worktree list --porcelain | grep -qxF "worktree $WT" \
  || die "refusing to mount $WT: not registered as a worktree of its repository"

# ── The prompt: a regular file inside the task directory ──
PROMPT_ROOT_IN="${FOREMAN_PROMPT_ROOT:-$HOME/.handoff/tasks}"
[ -d "$PROMPT_ROOT_IN" ] || die "prompt directory does not exist: $PROMPT_ROOT_IN"
PROMPT_ROOT="$(cd "$PROMPT_ROOT_IN" && pwd -P)"
[ ! -L "$PROMPT_IN" ] || die "refusing a symlinked prompt file: $PROMPT_IN"
[ -f "$PROMPT_IN" ] || die "prompt file does not exist: $PROMPT_IN"
PROMPT="$(cd "$(dirname "$PROMPT_IN")" && pwd -P)/$(basename "$PROMPT_IN")"
[ "$(dirname "$PROMPT")" = "$PROMPT_ROOT" ] || die "refusing a prompt outside $PROMPT_ROOT: $PROMPT_IN"

ctx=(); [ -n "${FOREMAN_DOCKER_CONTEXT:-}" ] && ctx=(--context "$FOREMAN_DOCKER_CONTEXT")
exec docker ${ctx[@]+"${ctx[@]}"} run --rm \
  --memory 4g --cpus 2 --pids-limit 512 \
  --cap-drop=ALL --security-opt no-new-privileges \
  --read-only --tmpfs /tmp:rw,size=512m --tmpfs /home/worker:rw,mode=1777,size=256m \
  --mount "type=bind,source=$WT,target=/work" \
  --mount "type=bind,source=$PROMPT,target=/prompt.md,readonly" \
  -e ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic \
  -e ANTHROPIC_AUTH_TOKEN="$DEEPSEEK_API_KEY" \
  -e ANTHROPIC_MODEL="$MODEL" \
  "$IMAGE" \
  -p "$(cat "$PROMPT")" --dangerously-skip-permissions --output-format text
