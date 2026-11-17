# Provenance

## What this is

`founder-ledger` is a clean-room build for task #202 ("Clean-room
founder-ledger micro-tool v1", H3 build, ranked #2 by task #136's re-rank of
`docs/BUILD-ONLY-ASSET-INVENTORY.md`). It is a standalone product repository,
not documentation of `openclaw/autonomy-harness`.

## Clean-room statement

`founder_ledger.py`, `tests/test_founder_ledger.py`, this `README.md`, and
this file were **written from scratch for this task**. No source file, code
fragment, string literal, or data table was copied from any pre-existing
repository, prior task's shipped code, or toolkit already present in the
worker's workspace. In particular:

- No code from `openclaw/decision-packs-public` (tasks #200/#201) was reused
  — that project is an unrelated content product (payment-rail comparison
  pages), not a ledger tool.
- No code from any prior "ledger" implementation was reused. The worker that
  built this had access only to this repository's worktree
  (`openclaw/autonomy-harness`, task branch
  `task/202-clean-room-founder-ledger-micro-tool-v1-`); the task brief's own
  text ("one-file ledger + registry for tracking your first $1,000",
  falsifier threshold, publish-to-fresh-repo pattern) was the only
  requirement input available in that sandbox — the referenced task #123/#124
  decision documents live in `openclaw/autonomy-mission`, which this worker's
  session was not permitted to read (workspace access was restricted to the
  single harness worktree). Everything beyond that one sentence of brief —
  the CLI shape, the Decimal-based money handling, the append-only ledger,
  the frozen-milestone-registry design, the milestone thresholds, the test
  suite — was designed independently for this build.
- A supervisor or operator verifying this claim can diff this project's
  history against every other project in the `openclaw` GitLab group and
  confirm no file in `founder_ledger.py` or `tests/test_founder_ledger.py`
  matches content elsewhere (e.g. `grep -r` across other project checkouts
  for distinctive strings from this file, such as `frozen permanently in the
  registry` or `MILESTONES_USD`).

## Build environment constraints (for the record)

The worker session that built this had no network access to fetch or verify
anything beyond the local worktree and the GitLab API for this group. No
outbound "market research" (checking whether a similarly named tool already
exists, checking npm/PyPI for name collisions, etc.) was performed as part of
this build; an operator or supervisor with live web access should do a quick
sanity check before wide publish.

## What the worker did and did not do

**Did:** wrote `founder_ledger.py`, its test suite, `README.md`, `LICENSE`
(MIT), and this file; ran the test suite locally (`python3 -m unittest
discover -s tests -v`, 9/9 passing); created the GitLab project
`openclaw/founder-ledger` via `lib/autonomy/gitlab.py`'s
`create_project()` (policy-gated via `policy/policy.json`'s
`gitlab.allow_create_projects`, not operator-gated — see `DECISIONS.md`
ADR-010 in `autonomy-harness` for why this class of action is worker-capable
while credential minting is not); pushed this content to `main`.

**Did not do (operator-only, same pattern as tasks #200/#201):**

1. **Visibility.** `create_project()` always creates projects as
   `visibility: "private"` (hardcoded in `lib/autonomy/gitlab.py`). This
   project is private until an operator changes it. The 30-day falsifier
   clock in `README.md` should be read as starting from **whenever an
   operator makes this repo public** (or otherwise externally discoverable),
   not from the push date below — record that date here once it happens.
2. **Any external publish or distribution.** No PyPI package, no landing
   page, no submission to a "awesome list" or tool directory, no tip-jar /
   payment link was created. `README.md` states the falsifier threshold
   (>= $1 earned, or >= 200 stars/installs in 30 days of being published)
   but nothing here wires up a way to actually collect a dollar yet — that
   requires a payment link, which is an operator or explicitly-scoped
   worker action, same reasoning as the decision-packs-public precedent.
3. **CI runner.** `.gitlab-ci.yml` in this project runs the test suite on
   push, but per the decision-packs-public precedent this GitLab instance
   has no registered runner (`GET /projects/:id/runners` returned `[]` as of
   task #201) — an operator needs to register one before this pipeline will
   actually execute rather than sit `pending`.

## Verification record

Push commit and verification command output are recorded in
`openclaw/autonomy-harness`'s `docs/OPERATOR-ACTIVATION-CARD.md`, task #202
entry, alongside the `git ls-remote` output confirming the pushed SHA.
