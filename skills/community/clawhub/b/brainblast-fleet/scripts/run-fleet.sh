#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Brainblast fleet — one deterministic sourcing cycle. HARNESS-AGNOSTIC.
#
# Sweeps Sourcegraph seams for silent SDK footguns → proves every candidate
# RED→GREEN through the real checkers (the absolute gate) → verifies the whole
# corpus still reproduces (SLA gate) → submits only the newly-proven ones to the
# open registry (which re-proves server-side) → optionally reproves.
#
# It needs NO model and NO GitHub quota: Sourcegraph streaming search returns
# repo + commit SHA + line (commit-pinned provenance), and the prove/SLA gates
# are deterministic. That is what makes it safe to run unattended on a cron. The
# OpenClaw / Hermes skills wrap this: the agent picks seams, runs it, reads the
# scoreboard, and reports — the gates below decide what actually lands.
#
# Robustness (why an unattended loop stays healthy):
#   • single-run lock       — overlapping ticks can't corrupt the shared clone
#   • managed-clone reset    — packs/ + candidates/ return to the committed
#                              baseline each run, so prove/SLA cost stays bounded
#                              and never creeps past the cron timeout. Guarded by
#                              a sentinel so it NEVER resets a repo it didn't clone.
#   • scoped submit          — only locally-PROVEN, newly-swept candidates are
#                              POSTed, so the registry's 60/hr per-IP cap is spent
#                              on new work, not on re-POSTing the committed corpus.
#   • hardened PATH + checks — cron envs are minimal; missing tools fail loudly.
#
# Every gate is absolute. A red gate aborts BEFORE anything is submitted. Nothing
# is ever hand-edited to force a pass — a non-reproducing candidate is a DRAFT.
#
# Usage:  run-fleet.sh [seam ...]     # default: --all seams
#         run-fleet.sh --list         # list seams and exit
# Env (all optional):
#   BRAINBLAST_REPO          managed checkout dir (default ~/.brainblast/repo).
#                            NOTE: a clone the fleet creates here is reset to its
#                            committed baseline every run — do NOT point this at a
#                            repo you are working in (the fleet detects its own
#                            clones via a sentinel and never resets anything else).
#   BRAINBLAST_REPO_REMOTE   git remote (default https://github.com/DSB-117/brainblast.git)
#   BRAINBLAST_INGEST_TOKEN  operator token — bypasses the 60/hr per-IP submit cap
#                            (server still gates on provenance + reproof).
#   BRAINBLAST_REPROVE       set to 1 to run `npm run reprove` after a batch so new
#                            VTIs flip proof_verified=true immediately (the registry
#                            also reproves on its own ~30-min schedule).
#   BRAINBLAST_REPROVE_TOKEN shared secret required by `npm run reprove`.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO="${BRAINBLAST_REPO:-$HOME/.brainblast/repo}"
REMOTE="${BRAINBLAST_REPO_REMOTE:-https://github.com/DSB-117/brainblast.git}"
# Sentinel lives INSIDE .git/ (which `git clean` never touches) so it survives the
# per-run reset and can't be confused with a user's own checkout.
SENTINEL_REL=".git/brainblast-fleet-managed"

# Cron shells inherit a minimal PATH — make node/npm/git/python findable.
export PATH="$PATH:/usr/local/bin:/opt/homebrew/bin:/usr/local/sbin:/usr/bin:/bin"

log() { printf '\n\033[36m▸ %s\033[0m\n' "$*"; }
die() { printf '\n\033[31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

for t in git node npm python3; do
  command -v "$t" >/dev/null || die "$t not found on PATH (cron PATH is minimal — install $t or extend PATH)"
done

# ── Single-run lock (mkdir is atomic + portable; no flock dependency) ────────
LOCK="${TMPDIR:-/tmp}/brainblast-fleet-$(printf '%s' "$REPO" | cksum | cut -d' ' -f1).lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +120 2>/dev/null)" ]; then
    log "stealing stale lock ($LOCK, >2h old)"
    rmdir "$LOCK" 2>/dev/null || true
    mkdir "$LOCK" 2>/dev/null || { log "lock contended — another run won; exiting"; exit 0; }
  else
    log "another fleet run holds the lock ($LOCK) — exiting cleanly"
    exit 0
  fi
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

# ── 1. Ensure the engine repo is present and current ─────────────────────────
# `git rev-parse` (not `-d .git`) so an existing worktree — where .git is a file,
# not a directory — is recognized instead of being re-cloned over.
if git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
  log "updating engine repo ($REPO)"
  git -C "$REPO" pull --ff-only 2>/dev/null || echo "  (pull skipped — local changes or offline; using current checkout)"
else
  log "cloning engine repo → $REPO"
  mkdir -p "$(dirname "$REPO")"
  git clone --depth 1 "$REMOTE" "$REPO"
  : > "$REPO/$SENTINEL_REL"   # mark this as a fleet-managed clone (safe to reset)
fi

CORE="$REPO/packages/core"
[ -d "$CORE" ] || die "packages/core not found in $REPO — wrong remote?"
cd "$CORE"

if [ ! -d node_modules ]; then
  log "installing engine deps (npm ci)"
  npm ci
fi

# --list short-circuits before any work.
if [ "${1:-}" = "--list" ]; then
  python3 "$REPO/fleet/scripts/sg_scout.py" --list
  exit 0
fi

SEAMS=("$@"); [ ${#SEAMS[@]} -eq 0 ] && SEAMS=(--all)

# ── 2. Reset the managed clone to its committed baseline ─────────────────────
# Keeps packs/ + candidates/ bounded so prove/SLA cost never creeps past the
# cron timeout. Guarded by the sentinel: a repo the fleet did NOT clone (e.g. a
# checkout you point BRAINBLAST_REPO at) is left completely untouched.
# `git clean` without -x keeps gitignored node_modules, so deps persist.
if [ -f "$REPO/$SENTINEL_REL" ]; then
  log "resetting managed clone to committed baseline"
  git -C "$REPO" reset --hard -q HEAD
  git -C "$REPO" clean -fdq
else
  log "unmanaged checkout — leaving the working tree as-is (no reset)"
fi

CANDIR="$REPO/fleet/candidates"
BEFORE="$(mktemp)"; ( ls "$CANDIR" 2>/dev/null | sort ) > "$BEFORE"

# ── 3. Discover — deterministic seam sweep, writes candidates ────────────────
log "scouting seams: ${SEAMS[*]}"
python3 "$REPO/fleet/scripts/sg_scout.py" "${SEAMS[@]}"

AFTER="$(mktemp)"; ( ls "$CANDIR" 2>/dev/null | sort ) > "$AFTER"
NEW=()   # candidate filenames this sweep added (bash 3.2-safe; no mapfile)
while IFS= read -r f; do [ -n "$f" ] && NEW+=("$f"); done < <(comm -13 "$BEFORE" "$AFTER")
rm -f "$BEFORE" "$AFTER"
log "${#NEW[@]} new candidate(s) from this sweep"

# ── 4. Prove + promote — the ABSOLUTE gate ───────────────────────────────────
# Non-reproducing candidates are reported DRAFT and never advance. `npm run
# fleet` exits 0 even when some draft (drafts are expected, not errors).
log "proving RED→GREEN + promoting (npm run fleet)"
npm run fleet

# ── 5. Corpus SLA gate — 100% reproduce or abort before any submit ───────────
log "corpus SLA gate (npm run sla)"
npm run sla || die "corpus SLA is RED — refusing to submit. Fix or drop the offending pack."

# ── 6. Submit only the newly-PROVEN candidates (respects the 60/hr per-IP cap) ─
# Parse this run's REPORT.md for PROMOTED/ALREADY verdicts, intersect with the
# sweep's new files. Submitting only new+proven avoids burning the cap re-POSTing
# the committed corpus and avoids wasting provenance fetches on local DRAFTs.
REPORT="$REPO/fleet/REPORT.md"
PROVEN=()
while IFS= read -r id; do [ -n "$id" ] && PROVEN+=("$id"); done < <(
  awk -F'|' 'NF>=5 && ($4 ~ /PROMOTED/ || $4 ~ /ALREADY/){gsub(/^[ \t]+|[ \t]+$/,"",$2); print $2}' "$REPORT" 2>/dev/null
)
# Match by exact filename (incl. .json) — sg_submit does substring matching, so a
# bare id could accidentally match a sibling candidate; "foo.json" cannot.
SUBMIT=()
for f in "${NEW[@]}"; do
  id="${f%.json}"
  for p in "${PROVEN[@]}"; do [ "$id" = "$p" ] && { SUBMIT+=("$f"); break; }; done
done

if [ ${#SUBMIT[@]} -gt 0 ]; then
  log "submitting ${#SUBMIT[@]} proven new candidate(s) to the registry (server re-proves)"
  python3 "$REPO/fleet/scripts/sg_submit.py" "${SUBMIT[@]}"
else
  log "no proven-new candidates this cycle — nothing to submit"
fi

# ── 7. Optional reprove — flip proof_verified=true now (registry also does ~30m)
if [ "${BRAINBLAST_REPROVE:-}" = "1" ]; then
  if [ -n "${BRAINBLAST_REPROVE_TOKEN:-}" ]; then
    log "reproving submissions (npm run reprove)"
    npm run reprove || echo "  (reprove failed — best-effort; the registry reproves on its own schedule)"
  else
    echo "  (BRAINBLAST_REPROVE=1 but BRAINBLAST_REPROVE_TOKEN unset — skipping; registry reproves every ~30m anyway)"
  fi
fi

log "cycle complete — see the scoreboard above for proven vs drafted counts"
