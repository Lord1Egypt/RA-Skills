---
name: address-review-comments
description: Address the latest reviewer comments on a PR with a pre-commit self-audit (consistency, regression-vs-history, staleness), then commit, push, and reply point-by-point. Accepts a PR number. Loop-aware — no-ops when there is nothing new and stops the loop when the reviewer gives the all-clear.
argument-hint: [pr-number]
metadata: { "openclaw": { "emoji": "🛠️", "requires": { "bins": ["gh", "jq", "git"] } } }
---

# Address review comments on a PR

Take the PR number from the user's request (or `$ARGUMENTS` on hosts that substitute it).
If it is not explicit, ask which PR before doing anything.

## Scope and autonomous actions (read before invoking)

Invoking this skill authorizes it to, without pausing for a per-step confirmation: edit
files on the PR branch, make one commit per review round, push that commit, and post one
GitHub PR reply comment per round through your `gh` credentials. It decides which round
to act on by matching PR comment CONTENT against a marker pattern (see Step 2), not by
authenticating who posted it beyond GitHub's own login attribution — anyone who can
comment on the PR (including, on some repos, the PR author replying to their own
automated review) can shape which comment this skill treats as "the latest reviewer
batch." Run it only on repositories where you trust everyone able to comment on a PR not
to forge a batch marker, and review the round's diff and reply before treating it as
final — this skill never merges or deploys, and a human is expected to do both. When it
ends a round by arming a wait for the next batch, that watch keeps running GitHub reads
(and, on a real batch, another edit/commit/push/comment round) after this invocation
ends, per whichever host mechanism `../WAITING.md` selects for your runtime; see that
file's host-mapping table for how to list, pause, or permanently stop it.

**Every command block below opens with this preamble, and that is deliberate.** Each
shell call may run in a *fresh process* — variables do not reliably survive from one block
to the next on every host — so a block that assumes `$PR` from an earlier one can run with
it empty. That is not a loud failure: `gh pr view ""` silently answers about the current
branch's PR, and a redirect built from an empty `$SCRATCH` targets `/`, which is
read-only. So every block re-derives `$PR` **and re-validates it** — a guard that runs
only in the illustrative preamble guards nothing, because the preamble is not what runs.
Re-derive, never carry over:

```bash
set -euo pipefail
PR="$ARGUMENTS"                       # substituted by the skill host, or set from the request
case "$PR" in ''|*[!0-9]*) echo "PR must be numeric, got '$PR'" >&2; exit 1 ;; esac
REPO=$(git rev-parse --show-toplevel) # the checkout that invoked this skill, not a path
SCRATCH="${TMPDIR:-/tmp}/pr${PR}-round"; mkdir -p "$SCRATCH"
```

`$SCRATCH` is derived from `$PR` rather than `mktemp -d` precisely so that re-deriving it
in a later block lands on the same directory. Worktrees for this repo's branches live
alongside it as `$REPO/../wt-*`.

## Review discipline (applies to every round)

A long adversarial review can diverge: each fix adds machinery, the machinery has its own
failure modes, and the document grows faster than findings close. Apply these rules to
any PR whose review has passed ~3 rounds:

1. **Freeze the threat model and architecture.** Introduce NO new mechanism
   unless it is required to fix a listed blocker. If a finding can be
   answered by tightening existing machinery, do that instead of adding a
   new component, principal, API, or state.
2. **One canonical home per contract.** Every actor/credential matrix,
   schema, and state machine lives in exactly ONE normative section, with a
   label (e.g. `C1`…`Cn`) indexed at the top of its section. Every other
   section — *especially* delivery-plan rows — REFERENCES the label and
   never restates the content. **A restatement is itself a defect.**
3. **Baseline with one frozen-head, full-system audit** that publishes every
   remaining blocker together, rather than discovering them serially.
4. **After that baseline, a new P1 is legitimate only if** it is (a) an
   unresolved listed blocker, (b) a regression introduced by a fix for one,
   or (c) a concrete high-impact path genuinely missed by the audit. Push
   back, with reasoning, on anything else.
5. **Underspecified operational detail is P2/follow-up, not P1.** "This
   could be more precisely specified" is not a blocker; "this cannot work
   as written" is.

When replying, state explicitly which category each finding falls into. If a
finding proposes new machinery on frozen architecture, say so and propose the
tightening instead.

## Standing rules (non-negotiable)

- **Never merge.** The repo owner merges after their own review. Never run `gh pr merge`.
- **One commit per review round**, pushed, then ONE reply comment. Never
  commit partial state mid-round.
- **Never chain a content-editing command and `git add/commit` in one shell
  command.** A failed edit must not let a commit of partial state through.
- Never print secrets in any file, commit, or comment.

## Step 1 — Resolve the worktree

```bash
set -euo pipefail
PR="$ARGUMENTS"
case "$PR" in ''|*[!0-9]*) echo "PR must be numeric, got '$PR'" >&2; exit 1 ;; esac
REPO=$(git rev-parse --show-toplevel)
# gh already derives the repo from the working directory; there is no flag for it.
gh pr view "$PR" --json headRefName,title,state --jq '"head=\(.headRefName) state=\(.state)"'
git -C "$REPO" worktree list
```

Work in the existing worktree that has the PR's head branch checked out. If none exists,
create it ANCHORED TO `$REPO` — `git worktree add "$REPO/../wt-<short-name>"
<headRefName>`. A bare `../wt-<name>` is relative to the working directory, so from a
subdirectory it lands *inside* the repo. Confirm the
worktree is clean before starting; if it has uncommitted changes, stop and
report — do not stack a new round on top of unexplained state.

## Step 2 — Fetch comments and decide the state (loop gate)

Dump the full comment history — and **all** of it means all three streams, every page.
You need it for the regression lens, and Step 2's whole decision is "is there a reviewer
batch newer than my last reply", which a short dump answers wrongly and silently.

`gh pr view --json comments` cannot do this, and its failure mode is the bad one. Verified
against the installed binary: it issues `comments(first: 100)` and returns them
**oldest-first**, so on a PR with 101 top-level comments the 100 you get are the 100 you
already know about and the newest reviewer batch is the one missing. Step 2 then reports
"waiting on reviewer" while a batch sits unaddressed. It also returns issue comments only,
never reviews or review replies, so the "all feedback" claim was never true of it.

```bash
set -euo pipefail
PR="$ARGUMENTS"
case "$PR" in ''|*[!0-9]*) echo "PR must be numeric, got '$PR'" >&2; exit 1 ;; esac
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
SCRATCH="${TMPDIR:-/tmp}/pr${PR}-round"; mkdir -p "$SCRATCH"
# Brace the variable: `pr$PR_all_comments.txt` expands to `pr.txt` — one undefined name,
# silently the wrong file.
OUT="$SCRATCH/pr${PR}_all_comments.txt"
# Write to a temp and move only on success. A failed page must not leave a SHORT history
# file behind, because a short file is exactly what this block exists to prevent and
# nothing downstream can tell one from a quiet PR.
{
  for ep in "issues/$PR/comments:comment" "pulls/$PR/reviews:review" "pulls/$PR/comments:reply"; do
    gh api --paginate --slurp "repos/$REPO/${ep%%:*}" \
      | jq --arg k "${ep##*:}" '[ .[][] | {kind:$k, who:.user.login, at:.created_at, body:(.body // "")} ]'
  done
} | jq -s -r '[.[][]] | sort_by(.at) | .[] |
      "=== \(.kind) by \(.who) @ \(.at) ===\n\(if .body == "" then "(no body — inline comments only)" else .body end)\n"' \
  > "$OUT.part"
mv "$OUT.part" "$OUT"
echo "dumped $(grep -c '^=== ' "$OUT") item(s) to $OUT"
```

`--slurp` yields an array of pages per endpoint, so `.[][]` flattens one endpoint and the
outer `jq -s` merges the three before sorting. `--slurp` cannot be combined with `--jq`,
which is why the filter is a separate `jq`.

**The regression check, because "it looked fine on a short PR" is how this shipped broken.**
Run it after any change to the block above; it stubs a second page and asserts the newest
batch survives:

```bash
set -euo pipefail
STUB=$(mktemp -d)
cat > "$STUB/gh" <<'GH'
#!/bin/sh
case "$*" in
  *"repo view"*)          echo "o/r" ;;
  *"issues/236/comments"*)
    { printf '[['
      i=1; while [ $i -le 100 ]; do
        [ $i -gt 1 ] && printf ','
        printf '{"user":{"login":"a"},"created_at":"2026-01-01T00:00:%02dZ","body":"old %d"}' $((i%60)) $i
        i=$((i+1))
      done
      printf '],[{"user":{"login":"a"},"created_at":"2026-09-10T05:11:44Z","body":"batch_id=NEWEST"}]]' ; } ;;
  *"pulls/236/reviews"*)  echo '[[]]' ;;
  *"pulls/236/comments"*) echo '[[]]' ;;
  *) echo "stub: unexpected: $*" >&2; exit 1 ;;
esac
GH
chmod +x "$STUB/gh"
PATH="$STUB:$PATH"; export PATH
PR=236; REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
{
  for ep in "issues/$PR/comments:comment" "pulls/$PR/reviews:review" "pulls/$PR/comments:reply"; do
    gh api --paginate --slurp "repos/$REPO/${ep%%:*}" \
      | jq --arg k "${ep##*:}" '[ .[][] | {kind:$k, who:.user.login, at:.created_at, body:(.body // "")} ]'
  done
} | jq -s -r '[.[][]] | sort_by(.at) | .[] | "=== \(.kind) by \(.who) @ \(.at) ===\n\(.body)\n"' \
  > "$STUB/dump.txt"
n=$(grep -c '^=== ' "$STUB/dump.txt")
[ "$n" -eq 101 ] || { echo "expected 101 items, got $n" >&2; exit 1; }
grep -q 'batch_id=NEWEST' "$STUB/dump.txt" \
  || { echo "the page-2 batch was dropped — the dump is not paginated" >&2; exit 1; }
echo "history pagination OK: 101 items, newest batch present and last"
rm -rf "$STUB"
```

It discriminates: on the same corpus, the first page alone yields 100 items with the newest
batch **absent**, and the paginated read yields 101 with it present and sorted last.

Identify the latest REVIEWER comment and the latest comment authored by us
(the reply posted last round). Then branch:

**Do not distinguish them by author.** The automated reviewer may post under the SAME
GitHub account as our replies, so `.user.login` cannot tell them apart. Distinguish by
content: reviewer batches carry a `<!-- review-pr-state … cycle=N … -->` metadata block;
our replies carry `codex-addressed:<batch_id>`.

If this round ends by waiting for the next batch, wait the way `../WAITING.md`
prescribes for your host — a background watch that costs little to nothing while the PR is
quiet, rather than a scheduler that re-runs this skill on a timer. That file holds the
loop, the host mapping, the filter-on-content rule and the filter-verification step; do
not restate them. Arm it with `MARKER='<!-- review-pr-state'` — the HTML comment the
reviewer writes, not the bare word, which appears in any reply discussing it, your own
included — and no `EXCLUDE`, since reviewer batches are what this direction waits for.
Bind `PR` and `REPO` into the command/prompt, since a watch may inherit nothing from this
session, and keep whatever id your host returns for stopping later.

1. **All-clear terminal state**: the latest reviewer comment states there are
   no further issues / nothing new to address / approves the design. Report
   this verbatim (quote the sentence). Do NOT edit, commit, or reply.
   **If running under a loop wrapper, end the loop now.**
2. **Nothing new**: no reviewer comment newer than our last reply. This
   iteration is a NO-OP — report "waiting on reviewer" and stop. If you are to
   keep waiting, arm the watch per `../WAITING.md` and stop; do NOT schedule a
   plain timed wakeup on top of it. A timed wakeup with no predicate re-runs this
   whole skill to discover nothing, which is the cost that file exists to remove.
3. **New findings**: the latest reviewer comment is newer than our last reply
   and contains findings. Proceed to Step 3.

Judge the all-clear by substance, not keywords: a comment that closes old
items but opens ANY new finding is state 3. A comment that only asks a
question for the repo owner (not a doc change) should be surfaced, not
"addressed" by editing.

## Step 3 — Apply the fixes (per-edit disk writes, asserted matches)

Enumerate every finding in the latest reviewer comment. For each one, locate
the exact current text (`grep -n` first — never edit from memory of the
file), then apply the edit.

Hard-won rules that exist because each was violated once and burned a round:

- **Every replacement must assert its match.** Use an edit tool that fails on
  a missed match, or a script that counts occurrences and reports each tag as
  applied/MISSED. A silent no-op edit reported as done is the worst failure
  mode this skill exists to prevent.
- **Write each edit to disk immediately** (per-edit writes). Batching edits
  in memory means one crash loses siblings that were already "done".
- A missed match is reported and retried with a re-read of current text —
  never dropped, never allowed to kill already-applied sibling edits.
- When a fix adds or changes a **shell command block inside a doc**, lint it
  as the target shell character by character: line-continuations (`\` must
  be last char), no inline `#` comments on continued command lines,
  `${VAR:+...}` is NOT an assignment in command position, arrays for
  conditional env/args. Paste the block into `zsh -n` (or your target
  shell's syntax-check mode) if there is any doubt.
- When a fix promises a test, add it to the matching workstream/test-inventory
  row in the same round — a promised-but-uninventoried test is a finding the
  reviewer WILL raise next round.

## Step 4 — Pre-commit self-audit (four lenses, adversarially verified)

Before committing anything, run a four-lens audit of the FULL revised
document/diff: one auditor per lens, each finding then adversarially verified
by a separate agent that defaults to "not real" when uncertain.

- **Lens 1 — internal consistency**: contradictions introduced by this
  round's edits; every grammar/contract (naming schemes, numeric budgets,
  actor assignments, config keys) checked against every usage site; shell
  blocks re-linted.
- **Lens 2 — regression vs reviewer history**: read the FULL comment dump
  from Step 2. For each previously-resolved finding, verify this revision
  did not reintroduce it or weaken its resolution.
- **Lens 3 — staleness + incompleteness**: leftover references to concepts
  this round changed; promised tests missing from workstream rows; any new
  mechanism named without who-runs-it / when / what-failure-it-produces.
- **Lens 4 — platform fact-check (give this lens web access)**: every
  claim the revision makes about a third-party platform — API endpoint,
  state/enum name, allowed state transition, CLI subcommand, UI control label,
  documented precondition — verified against the vendor's own current docs,
  and the verifier told to research independently rather than trust the
  auditor's citation.

  **This lens exists because it catches what the other three structurally
  cannot.** Prose review confirms a document is self-consistent; it cannot
  tell you the platform doesn't work that way. Invented-platform-behaviour
  blockers (a nonexistent CLI verb, a state transition that's actually
  unreachable from the claimed precondition, a UI control mislabelled) have
  cost real rounds on real PRs, sometimes ones that would have deadlocked a
  lane in production while reading perfectly coherently.

  Rules that follow from that: a wrong platform fact is a BLOCKER, not P2 —
  it cannot work as written. Never assert store/tool behaviour from memory;
  if you cannot verify it, say so in the document and route it to P2 rather
  than stating it. When a fact-check forces you to *reduce* claimed
  automation (an action that exists only in a vendor's web UI, not its API),
  reduce it — a design that promises a step which cannot run is worse than
  one that names the manual step honestly. And re-check your own
  corrections: over-correcting an already-wrong fact is a distinct failure.

Fix every CONFIRMED finding (same per-edit rules as Step 3), then run
residual greps for the vocabulary the round changed (old names, old numeric
values, old actor assignments) to catch stragglers the agents missed.

**Re-audit until the findings stop being consequential, not until zero.** If a
pass produced blocker-level fixes, audit the result again — the fix text is the
newest and least-reviewed text in the document, and in practice it carries its
own defects. Long-running review docs have needed six or more passes in a
single round, where each later pass found a real blocker created or left
behind by the previous pass's fix (a stale third copy of a rule, a deadlock
introduced by a new constraint, an invented platform fact, a clause that
re-attached to the wrong branch when a sentence was split).

Two rules keep that from becoming an infinite loop:

- **Scope each later pass to the text the previous pass changed**, not the whole
  document — a full re-sweep re-litigates settled sections and buries the real
  finding. Tell the auditors what is already fixed and to report nothing else;
  an empty result is the welcome outcome, and say so in the prompt.
- **Stop when the remaining findings are precision rather than correctness**,
  and list them explicitly as P2/follow-up in the reply. Reaching zero findings
  on prose is not the goal; the goal is that nothing left can deadlock,
  contradict, or mislead an implementer. Iterating past that point is the same
  divergence this discipline exists to end — just relocated from the reviewer
  into your own audit.

Watch for these two self-inflicted patterns specifically, because both recur:
inserting a clause mid-sentence and orphaning the trailing clauses onto the
wrong subject (re-read every edited sentence start-to-finish), and fixing a rule
in one place while an older copy survives elsewhere (grep the whole document for
the rule's distinctive vocabulary, not just the section you edited).

## Step 5 — Commit, push, reply

Single commit on the PR branch. Message: one line summarizing the round
(e.g. `E2E design: address review round N (6 findings)`), then push.

Then post ONE reply comment — write the body to a file first, because these are long and
shell-quoting them corrupts them:

```bash
set -euo pipefail
PR="$ARGUMENTS"
case "$PR" in ''|*[!0-9]*) echo "PR must be numeric, got '$PR'" >&2; exit 1 ;; esac
SCRATCH="${TMPDIR:-/tmp}/pr${PR}-round"
gh pr comment "$PR" --body-file "$SCRATCH/reply.md"
```

The reply contains:

- Per-finding numbered responses, each quoting the reviewer's anchor phrase
  and stating exactly what changed (with the new text or its location).
- Note anything the self-audit caught and fixed beyond the reviewer's list.
- Note anything deliberately NOT changed and why (e.g. a question routed to
  the repo owner instead).
- End by requesting another review pass.

## Step 6 — Report

State which round this was, the findings addressed, what the self-audit
caught, the commit SHA, and that the reply is posted. If anything needs a
decision (open questions, scope calls), list it explicitly.
