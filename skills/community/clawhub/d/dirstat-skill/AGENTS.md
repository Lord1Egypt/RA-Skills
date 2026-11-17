# AGENTS.md

## Primary Skill

For read-only disk-usage analysis and human review suggestions, load:

- `SKILL.md`

## Start Here

Before doing anything else, read:

- `README.md`

If a local `.agent/HANDOFF.md` exists in the working copy, use it as volatile operator memory only. Do not depend on it for the public repository workflow.

## Core Rule

This repository is read-only.

It does **not** change files automatically.
It does **not** issue cleanup commands.
It only scans, summarizes, and suggests what a human should review.

If the user sounds like this, this repo is the intended path:

- "I am tired of huge AI caches"
- "Which old models deserve review?"
- "What is wasting disk space?"
- "Show me the biggest junk on C: or D:"
- "Audit this Linux box without deleting anything"

## Runtime Scope

- Windows local paths via native Python scanner
- Linux local paths via `ncdu`
- remote orchestration is fine, but each filesystem must still be scanned by the host that owns it
- optional Linux helper scripts under `scripts/linux/`

## Expected Behavior

- use the generic CLI first:
  - `scan`
  - `summarize-export`
  - `audit`
- use `scripts/linux/` only for Linux convenience flows
- use `scripts/windows/` only for Windows convenience flows
- read compact outputs before raw exports
- read `review_report.md` before the diagnostic CSV files
- treat the dossier as analysis-driven:
  - `dominant space`
  - `path safety`
  - `nearby references`
  - `signature heuristics`
  - `probable duplicates`
  - `protected huge hotspots`
- use attention levels:
  - `review first`
  - `review carefully`
  - `keep protected`
- require a reason, evidence summary, and confidence level for every finding
- prefer partial downloads, trash, and cache as first review targets
- do not suggest touching Docker storage, swap, or obvious system paths blindly
- do not assume the whole machine must be scanned; prefer explicit `--path` targets
- fail loudly on invalid engine/platform/path combinations
- support runtime override of `--dominant-percent` when the current machine needs a wider or narrower dominant-space walk

