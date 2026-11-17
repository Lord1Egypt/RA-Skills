# DirStat_Skill Recursive Review Report Design

## Goal

Refactor the reporting stage so each audit run writes a complete review dossier under `outputs/` that explains which full paths deserve review, why they were selected, and what dependency checks were performed before assigning a review bucket.

## Problem

The current reporting layer is still shaped like a classic `top_n` summary:

- it privileges the globally largest directories and files
- it can miss many medium-size files that are individually below the top list but collectively dominate space
- it does not emit a final human-readable document that clearly justifies each review recommendation
- it does not record a dependency-check trace that explains why a path is treated as safe-ish, uncertain, or protected

The next version must move from `top_n` ranking to a recursive, evidence-based candidate dossier.

## Scope

This refactor applies to the report generation stage only. It must work with both supported raw-export engines:

- Windows native scanner
- Linux `ncdu`

It remains strictly read-only:

- no file removal
- no file mutation outside the chosen `outputs/<stamp>_audit/` bundle
- no mandatory online or LLM dependency

## Output Contract

Each audit run must continue to create a run folder under `outputs/<stamp>_audit/`, but the compact report bundle expands to:

- raw export file
- `summary.md`
- `top_dirs.csv`
- `top_files.csv`
- `candidates.json`
- `review_candidates.csv`
- `review_report.md`
- `run.log`

Optional supporting artifacts may be added if they are useful and deterministic, but the files above are the required public contract.

## Required Candidate Fields

Every candidate record in `candidates.json` and `review_candidates.csv` must include at least:

- `path`
- `dsize`
- `is_dir`
- `bucket`
- `review_reason`
- `dependency_check_summary`
- `dependency_check_confidence`
- `selection_source`

### Field Semantics

- `review_reason`
  - plain-language explanation of why this path is in the review dossier
  - examples:
    - `partial download file`
    - `trash subtree dominates 92% of parent space`
    - `cache directory selected by recursive 80/20 walk`
    - `model asset under user-owned path with no nearby references found`
- `dependency_check_summary`
  - plain-language summary of what was checked
  - examples:
    - `matched cache/temp signature; no nearby manifests or workflow refs found`
    - `path is under ComfyUI models; nearby workflow/config references not found`
    - `system-owned storage path protected by policy`
- `dependency_check_confidence`
  - compact confidence level for the dependency verdict
  - allowed values:
    - `high`
    - `medium`
    - `low`
- `bucket`
  - allowed values:
    - `review first`
    - `review carefully`
    - `keep protected`
- `selection_source`
  - shows how the candidate entered the dossier
  - examples:
    - `root`
    - `top_file`
    - `dominant_subtree`
    - `dominant_leaf`

## Recursive 80/20 Selection Algorithm

The new selector must stop behaving like a flat leaderboard.

### Phase 1: Root Ranking

For each scan root:

- build the immediate child distribution
- sort children by `dsize`
- keep descending through children until the cumulative size reaches at least `80%` of the parent
- mark those children as dominant branches

### Phase 2: Recursive Branch Refinement

For each dominant branch:

- if the branch is a directory, repeat the same `80%` selection within that directory
- if a branch collapses to a small set of concrete large files, emit those files as candidates
- if a branch remains a mixed directory, keep descending while the branch continues to explain a dominant fraction of its parent

### Phase 3: Stop Rules

Stop descending when any of the following becomes true:

- the node is a file
- the directory has no children in normalized data
- the directory is below the configured minimum bytes threshold
- the directory is already classified as `keep protected`
- the child distribution is too flat to produce a meaningful dominant subset

When the distribution is too flat, the directory itself remains a candidate so the dossier still captures the aggregate waste pattern.

## Completeness Rule

The selector must not arbitrarily cap the report at “the biggest 10 files”.

Instead:

- follow the recursive `80%` rule per dominant subtree
- include all emitted candidates produced by that walk
- keep `top_dirs.csv` and `top_files.csv` as diagnostic summaries, not as the final review contract

This means one run can legitimately output many candidates when a large subtree is composed of many medium-size deletable files.

## Dependency Check Strategy

The default dependency check mode is:

- `heuristic + nearby refs`

The report must evaluate each candidate with two layers:

### Layer 1: Heuristic Check

Always perform:

- path sensitivity check
- extension and basename signature check
- risk bucket policy check
- known cache/trash/temp/partial markers
- known protected system locations

### Layer 2: Nearby Reference Check

For paths not immediately classifiable as cache/trash/system:

- inspect the candidate directory and a small number of ancestor directories
- search for nearby manifests, configs, workflow files, or lists that may reference the asset
- examples of useful nearby signals:
  - `.json`
  - `.yaml`
  - `.yml`
  - `.txt`
  - `.md`
  - workflow definitions
  - model list files
  - launch scripts

The check is intentionally local and cheap. It must not scan the entire repository or entire disk by default.

## Escalation Rule

The skill or agent using the repository may optionally escalate to a broader scan only for ambiguous macrofolders.

Examples:

- giant user model directories
- application input stores
- custom data folders with unclear ownership

This escalation is discretionary and not the default reporting path.

## `review_report.md`

The report must be directly readable by a human with no extra tooling.

### Required Sections

- run metadata
- roots scanned
- dominant branches discovered by the recursive walk
- `review first`
- `review carefully`
- `keep protected`
- dependency-check notes
- next-step recommendations

### Candidate Rendering Format

Each candidate entry in `review_report.md` must contain:

- full path
- size in bytes and human-readable size
- reason for selection
- dependency check summary
- final review bucket

## Config Additions

`config/defaults.json` should be extended with deterministic knobs for the new reporting logic, for example:

- `dominant_percent`: `0.8`
- `min_candidate_bytes`
- `max_nearby_reference_files`
- `nearby_reference_extensions`

These values must be configurable but should ship with sane defaults.

## Logging

`run.log` must record the major reporting decisions:

- root distribution analysis
- dominant branch selections
- stop reasons during recursion
- dependency-check signals found
- total candidates emitted

## Testing

Automated tests must cover:

- recursive `80%` selection over a directory tree with mixed file sizes
- directory stop conditions
- dossier completeness when many medium files dominate together
- candidate reason generation
- dependency-check summaries for:
  - cache/temp/trash
  - user asset with no nearby refs
  - protected system path
- `review_report.md` generation
- `review_candidates.csv` generation

## Non-Goals

- deleting files automatically
- deep semantic dependency analysis across the entire machine
- file-content parsing for every binary format
- LLM-based reasoning during report generation

