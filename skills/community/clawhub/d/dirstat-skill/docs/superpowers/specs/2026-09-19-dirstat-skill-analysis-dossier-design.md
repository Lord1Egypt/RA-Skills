# DirStat_Skill Analysis Dossier Design

## Goal

Refactor the public reporting contract so `DirStat_Skill` explains disk findings as explicit analysis types instead of the current three-category-only presentation.

## Why

The real DGX run exposed two product gaps:

- probable duplicates are not surfaced explicitly
- protected but huge runtime areas are hidden behind protection rules instead of being reported as hotspots

The repository must stay read-only, cross-platform, and safe, but the dossier must become more informative and easier for humans and agents to interpret.

## Hard Constraints

- public wording must avoid frightening action verbs such as `delete` and `remove`
- the runtime remains read-only
- Windows and Linux ARM64 must both stay supported
- the current runtime guardrails must remain intact
- `dominant_percent` must be configurable at runtime instead of being effectively fixed to config-only behavior

## Public Output Model

The dossier stays compact but becomes analysis-driven.

Required analysis types:

1. `dominant space`
2. `path safety`
3. `nearby references`
4. `signature heuristics`
5. `probable duplicates`
6. `protected huge hotspots`

The output files remain:

- `summary.md`
- `top_dirs.csv`
- `top_files.csv`
- `candidates.json`
- `review_candidates.csv`
- `review_report.md`
- `run.log`

## Finding Model

Each finding in `candidates.json` and `review_candidates.csv` must include:

- `path`
- `dsize`
- `is_dir`
- `analysis_kind`
- `attention_level`
- `review_reason`
- `evidence`
- `dependency_check_confidence`
- `selection_source`
- `group_key`
- `configured_dominant_percent`

### Field Rules

- `analysis_kind`
  - one of the six public analysis types above
- `attention_level`
  - keeps the existing public levels:
    - `review first`
    - `review carefully`
    - `keep protected`
- `evidence`
  - concise machine-readable or human-readable proof summary
  - examples:
    - `same basename and same size across two directories`
    - `protected prefix matched with 77 GB subtree`
    - `matched partial-download suffix`
- `group_key`
  - ties related findings together
  - examples:
    - duplicate cluster id
    - hotspot cluster id
    - empty string when not grouped
- `configured_dominant_percent`
  - the actual dominant-space threshold used for this run

## Reporting Rules

`review_report.md` must teach interpretation directly.

It should contain:

- run metadata
- configured dominant threshold
- short interpretation guide
- six analysis sections in a fixed order
- per-finding evidence and confidence
- explicit limitations section

The report must tell the reader:

- what the analysis means
- why the path appeared
- how reliable the signal is
- whether human judgment is still required

## Duplicate Detection

The default duplicate detector must be fast and cross-platform.

Phase 1:

- candidate set limited to large user-owned asset files
- group by:
  - basename
  - file size
  - extension
- only keep groups that appear in different directories

This is a `probable duplicates` analysis, not a cryptographic proof. No content hash is required in the standard path.

## Protected Huge Hotspots

Protected areas must remain protected, but very large protected paths must no longer disappear from the dossier.

Rules:

- if a selected node matches a protected prefix and exceeds the configured minimum candidate threshold, surface it under `protected huge hotspots`
- keep `attention_level = keep protected`
- explain that the path is operationally sensitive but space-heavy

## Runtime Configuration

`dominant_percent` must support:

- default from `config/defaults.json`
- runtime override through the CLI
- documentation in `README.md`, `AGENTS.md`, and `skills/DirStat_Skill/SKILL.md`

The runtime override is intended for agent use and advanced runs. The default remains `0.8`.

## Documentation Requirements

`README.md`, `AGENTS.md`, and `SKILL.md` must all explain:

- how to read the dossier
- what each analysis type means
- what not to infer from a low-confidence result
- how to override `dominant_percent`
- that the workflow is interpretation-first and read-only

## Testing Requirements

Automated tests must cover:

- runtime config override of `dominant_percent`
- report render with the new analysis sections
- probable duplicate detection with same basename and same size in different directories
- protected huge hotspot detection for Linux protected paths
- protected huge hotspot detection logic remaining compatible with Windows protected prefixes
- no regression in runtime guardrails

Manual verification must include:

- Windows-friendly CLI path
- Linux/DGX path
- OpenClaw symlink still resolving to `skills/DirStat_Skill`
