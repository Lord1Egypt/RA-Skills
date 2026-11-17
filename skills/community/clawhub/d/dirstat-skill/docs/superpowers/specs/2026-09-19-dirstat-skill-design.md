# DirStat_Skill Design

## Goal

Build a public, GitHub-ready repository and agent skill that audits disk usage in a read-only way on both Windows and Linux, produces compact AI-friendly summaries, and suggests what a human should review to reclaim space without performing any removal automatically.

## Scope

The next version is:

- cross-platform: Windows workstation and Linux hosts, including ARM64 DGX
- read-only by default
- path-driven: the operator passes one or more target roots such as `C:\`, `D:\`, `F:\`, `/`, or `/home`
- optimized for low-token AI review
- packaged as one reusable skill, not as a machine-specific workflow

The next version is not responsible for removing files automatically.

## Supported Runtime Model

- repository location: standard GitHub repository with generic docs and skill packaging
- supported local runtime on Windows: Python 3.12+ using stdlib filesystem access
- supported local runtime on Linux: Python 3.12+ plus `ncdu` when the Linux engine is selected
- supported targets:
  - Windows local drives and mounted volumes
  - Linux local filesystems
  - user-provided target paths on either platform

The repository must stop describing itself as DGX-first. DGX remains a valid Linux ARM64 target, but no longer defines the public product identity.

## Official Design Inputs

The cross-platform scanner design is grounded in official Python documentation:

- Python `os` provides portable operating-system interfaces and raises `OSError` on invalid or inaccessible paths
- Python 3.12 adds Windows-specific `os.listdrives()`, `os.listvolumes()`, and `os.listmounts()` for enumerating drives and mount points
- `os.scandir()` provides directory entries with file attribute information and is the preferred low-level primitive for efficient tree walking
- `shutil.disk_usage(path)` provides total, used, and free bytes for the filesystem containing a path
- `pathlib.Path` is the standard high-level path abstraction for the current platform

These are sufficient to build a generic Windows scanner without requiring third-party Windows-only tools in `v2`.  
Sources:

- [Python `shutil.disk_usage`](https://docs.python.org/3.12/library/shutil.html#shutil.disk_usage)
- [Python `os` module](https://docs.python.org/it/3.12/library/os.html)
- [What’s New in Python 3.12: `os.listdrives()` / `os.listvolumes()` / `os.listmounts()`](https://docs.python.org/el/3/whatsnew/3.12.html)
- [Python `pathlib`](https://docs.python.org/3/library/pathlib.html)

## Core Principles

1. Keep the repository generic and portable.
2. Keep raw scan data on disk and out of LLM context by default.
3. Separate engine-specific scan logic from normalization and reporting.
4. Make the first review pass compact and risk-ranked.
5. Suggest review only; never remove files automatically.
6. Accept explicit target paths instead of assuming a machine-wide default root.

## High-Level Architecture

The system consists of five layers:

- `target selection`
  - accepts one or more roots from the operator
  - resolves whether to scan a Windows path, Linux path, or auto-discovered local volume
- `scan engine adapter`
  - platform-specific raw enumeration
  - writes raw export data to disk
- `normalizer`
  - converts raw engine output into one stable internal structure
- `risk classifier`
  - applies rules that detect sensitive paths, probable runtime ownership, and obvious danger zones
- `report generator`
  - emits compact outputs for AI and human review

Only the `scan engine adapter` and parts of target discovery are platform-specific.

## Engine Strategy

### Windows Engine

Windows support should use a native Python engine in `v2`.

- default enumeration uses `os.scandir()` and `pathlib.Path`
- filesystem capacity uses `shutil.disk_usage(path)`
- local drive discovery uses `os.listdrives()` on Python 3.12+
- explicit operator paths remain the primary input, even when auto-discovery is available

Why this choice:

- no mandatory third-party dependency
- portable for ordinary Windows users
- testable on the developer workstation
- compatible with public GitHub distribution

### Linux Engine

Linux support keeps `ncdu` as the preferred engine when available.

- `ncdu` remains appropriate for headless Linux and large trees
- the repository does not vendor `ncdu`
- Linux wrappers remain supported, but they must be documented as Linux helpers rather than as the core public identity

## CLI Design

The CLI should move from a Linux-specific summarizer into a generic interface:

- `DirStat_Skill scan --path C:\ --path D:\`
- `DirStat_Skill scan --path / --engine ncdu`
- `DirStat_Skill summarize-export --export <raw-export> --output-dir <run-dir>`
- `DirStat_Skill audit --path C:\`

Behavior:

- `scan` creates a raw export only
- `summarize-export` converts an existing raw export into compact reports
- `audit` performs scan plus summarize in one command

Auto-detection defaults must be deterministic:

- on Windows: use the native Python engine
- on Linux: use the `ncdu` engine if available, otherwise fail with a clear missing-engine error

The CLI must allow explicit override for reproducibility.

## Raw Export Contract

Each engine may write a different raw format, but normalization must converge to one internal model with:

- normalized path
- base name
- node type: file or directory
- apparent size
- descendant size or aggregate size
- optional engine metadata

The current normalized report format remains valid and should be reused rather than reinvented.

## Token Strategy

Token control remains a first-class design requirement.

The workflow must:

- keep raw exports on disk
- generate compact summaries before AI review
- limit first-pass analysis to top `N` and size thresholds
- support path-by-path drill-down instead of whole-tree ingestion
- allow targeted scanning of one or more chosen roots rather than blindly scanning every mounted filesystem

The workflow must not:

- paste the complete raw scan into the LLM
- recursively expand all subtrees by default
- assume that “all disks” should always be scanned in one pass

## Repository Layout

- `skills/DirStat_Skill/SKILL.md`
  - public skill entrypoint
- `AGENTS.md`
  - repository-level pointer for agent users
- `config/`
  - thresholds, exclusions, risk rules, engine settings
- `docs/superpowers/specs/`
  - design documents
- `docs/superpowers/plans/`
  - implementation plans
- `scripts/linux/`
  - Linux operational wrappers
- `scripts/windows/`
  - Windows helpers only when a helper script adds value
- `src/`
  - engine adapters, normalization, classification, reporting, CLI
- `tests/`
  - focused tests for parser, engine, policy, and CLI behavior
- `outputs/`
  - dated run folders
- `.agent/`
  - local-only operator memory and research, ignored from git

## Output Contract

Each audit run should create a dated folder under `outputs/` containing at least:

- raw scan export
- `summary.md`
- `top_dirs.csv`
- `top_files.csv`
- `candidates.json`

This output contract stays platform-independent.

## Risk Model

Each shortlisted path should be placed into one of three review buckets:

- `review first`
- `review carefully`
- `keep protected`

Classification should consider:

- size
- path sensitivity
- obvious cache or trash signatures
- probable runtime ownership
- whether the path belongs to system areas, application inputs, package stores, or user caches
- whether a path was explicitly requested by the user or auto-discovered

The Windows ruleset must add common Windows danger zones such as:

- `C:\Windows`
- `C:\Program Files`
- `C:\Program Files (x86)`
- package manager stores and system-owned locations

The Linux ruleset continues to protect:

- `/etc`
- `/usr`
- `/boot`
- `/var/lib`
- swap and Docker-backed storage

## Error Handling

The implementation must fail loudly when:

- the target path does not exist
- the scan engine is missing
- the raw export format is unsupported
- the output directory cannot be created
- an inaccessible subtree prevents complete traversal and the engine cannot recover cleanly

Errors and warnings should be surfaced in logs and summarized in the final report rather than silently swallowed.

## Logging

The implementation should add structured run logging with lines formatted as:

- `[INFO] | 2026-09-19T14:05:00Z | scan.windows | ...`
- `[WARN] | 2026-09-19T14:05:00Z | reporting | ...`
- `[ERROR] | 2026-09-19T14:05:00Z | engine.ncdu | ...`

The log file should live inside each dated run directory.

## Testing Strategy

Automated tests should cover:

- Windows path normalization behavior
- Linux path normalization behavior
- engine selection logic
- raw-to-normalized conversion on small sample exports
- threshold filtering
- risk bucket assignment
- summary generation correctness
- CLI behavior for `scan`, `summarize-export`, and `audit`

Manual verification should confirm:

- Windows audit runs on at least two local volumes if available
- Linux audit still works on ARM64 DGX
- summaries remain compact
- no removal operation is performed
- the skill instructions match the actual CLI and scripts

## Migration Constraints

The repository already contains Linux-specific code and DGX wrappers.

`v2` should preserve working Linux behavior while broadening the product:

- keep existing Linux functionality green while refactoring
- move Linux wrappers into a clearly named Linux area
- update README, AGENTS, and SKILL so they describe one global skill
- keep the Python import package `dirstat_skill` stable unless a rename is strictly necessary

## Recommended Next Step

Write an implementation plan for:

- generic engine abstraction
- Windows native scanner
- Linux engine preservation
- generic CLI refactor
- cross-platform risk rules
- Windows and Linux verification
- documentation rewrite for public GitHub usage



