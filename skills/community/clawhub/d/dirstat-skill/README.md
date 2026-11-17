# DirStat_Skill

> READ-ONLY ANALYSIS ONLY
>
> `DirStat_Skill` never changes files automatically, never schedules cleanup, and never performs destructive actions.
> It only scans disk usage, builds compact reports, and suggests what a human should review.

Tired of wasting tens of GB on forgotten AI models, bloated caches, and files you have not touched since the Cold War? This is the safe read-only answer.

## Goal

`DirStat_Skill` is a public, cross-platform disk-usage analysis skill and repository.

It helps humans and agents:

- scan explicit paths on Windows or Linux
- keep raw scan data on disk instead of dumping it into an LLM
- generate compact summaries first
- follow dominant branches recursively with a configurable dominant-space walk
- present findings as explicit analysis types plus attention levels
- produce a review dossier with reasons, evidence, and confidence notes

## Identity

- public repository name: `DirStat_Skill`
- skill path: `SKILL.md`
- repository agent entrypoint: `AGENTS.md`
- Python package: `dirstat_skill`

## Runtime Matrix

- Windows filesystem on Windows host:
  - run `python -m dirstat_skill.cli audit ...`
  - engine: `windows-native`
- Linux filesystem on Linux host:
  - run `python3 -m dirstat_skill.cli audit --engine ncdu ...`
  - engine: `ncdu`
- Remote or mixed-machine workflow:
  - run the scan on the machine that owns the filesystem
  - move only the compact outputs elsewhere if you want another agent or host to review them
  - if a Linux or DGX host already has remote shell access to a Windows host, launch `windows-native` on that Windows host and only bring back the compact outputs
  - do not fake a Windows scan from Linux with a mismatched runtime

## Hard Guardrails

The CLI now fails loudly when the runtime contract is wrong:

- `windows-native` outside Windows: blocked
- `ncdu` on Windows: blocked
- Windows-style paths with Linux runtime: blocked
- Linux-style paths with Windows runtime: blocked

This is intentional. The skill is supposed to be idiot-proof, not permissive.

## Token Strategy

- raw exports stay on disk
- the first pass reads `review_report.md`, `review_candidates.csv`, `summary.md`, and `candidates.json`
- reviews start from dominant branches, not from a flat global top list
- drill-down happens path by path with a configurable dominant-space walk
- agents read raw exports only when compact outputs are missing or inconsistent

## Output Contract

Every audit run writes a bundle under `outputs/<stamp>_audit/`:

- raw export file
- `summary.md`
- `top_dirs.csv`
- `top_files.csv`
- `candidates.json`
- `review_candidates.csv`
- `review_report.md`
- `run.log`

## Runtime Overrides

The dominant-space selector is configurable:

- default: `dominant_percent = 0.8` from `config/defaults.json`
- runtime override:

```bash
python -m dirstat_skill.cli audit --path C:\ --output-dir outputs\win_c_audit --config config\defaults.json --dominant-percent 0.67
python3 -m dirstat_skill.cli audit --path /home --engine ncdu --output-dir outputs/linux_home_audit --config config/defaults.json --dominant-percent 0.72
```

Use the default for normal runs. Override it only when an agent or operator needs a wider or narrower dominant-space walk for the current machine.

## Installation

### Python

```bash
python -m pip install -e .
```

### Linux `ncdu`

Install `ncdu` with your distribution package manager or use `scripts/linux/install_ncdu.sh`.

## Quick Start

### Windows

```bash
python -m dirstat_skill.cli audit --path C:\ --output-dir outputs\win_c_audit --config config\defaults.json
```

Multiple targets:

```bash
python -m dirstat_skill.cli audit --path C:\ --path D:\models --output-dir outputs\win_multi_audit --config config\defaults.json
```

### Linux

```bash
python3 -m dirstat_skill.cli audit --path /home --engine ncdu --output-dir outputs/linux_home_audit --config config/defaults.json
```

### Linux Helper Scripts

```bash
bash scripts/linux/prepare_linux_scripts.sh
bash scripts/linux/run_audit.sh /home
```

### Windows Helper Script

```powershell
powershell -ExecutionPolicy Bypass -File scripts/windows/run_audit.ps1 -TargetPath C:\ -OutputDir outputs\win_c_audit
```

## Analysis Types

- `dominant space`
  - paths that explain most space under the current dominant threshold
- `path safety`
  - paths whose location changes how cautiously they must be interpreted
- `nearby references`
  - paths with nearby manifests, configs, or local evidence worth reading
- `signature heuristics`
  - cache, temp, trash, and incomplete-download patterns
- `probable duplicates`
  - same basename + same size + same extension across different directories
- `protected huge hotspots`
  - very large protected areas that must stay visible in the dossier

Attention levels still stay compact:

- `review first`
- `review carefully`
- `keep protected`

## Review Dossier

- `review_report.md`
  - human-readable dossier
  - grouped by analysis type
  - includes full paths, reasons, evidence, confidence, and attention levels
- `review_candidates.csv`
  - structured flat export for spreadsheets and scripts
- `candidates.json`
  - machine-readable version for agent workflows

### Example Report Snapshot

The compact dossier is meant to read like this:

```text
Root: F:\
Total scanned: 3.70 TB

Dominant space
- F:\SteamLibrary -> 1.68 TB
- F:\huggingface_cache -> 402 GB
- F:\PROGRAMS\ComfyUI\models -> 281 GB

Probable duplicates
- flux1-dev-fp8.safetensors -> 17.25 GB x2
  evidence: same basename, same size, different directories
- silicon-maid-7b.gguf -> 4.37 GB x3
  evidence: same basename, same size, different directories

Signature heuristics
- F:\GAMES\ZIPPED\2025.10.17_Shipping_Full_Build_1_AA.zip -> 19.7 GB
  reason: archive appears redundant because extracted content exists nearby
- F:\huggingface_cache\... -> 402 GB
  reason: redownloadable model cache under a cache-like path

Keep protected
- F:\docker\wsl\data\docker_data.vhdx -> 90 GB
  reason: protected runtime-owned storage, keep visible but do not treat as an easy review target
- F:\pagefile.sys -> 41 GB
  reason: system paging file
```

That is the point of the repository: not just a raw top list, but a compact English dossier with:

- full paths
- concrete sizes
- analysis type
- evidence for why the path was surfaced
- an attention level that stays readable for humans and agents

Real runs also make product gaps visible. For example, if a path like `trash\` or `huggingface_cache\` is not surfaced by the signature heuristics, that is a tooling gap worth fixing rather than a reason to trust the output blindly.

### How To Read Results

Read in this order:

1. `review_report.md`
2. `review_candidates.csv`
3. `summary.md`
4. `candidates.json`

Interpretation rules:

- start with `dominant space`
- use `probable duplicates` as a strong suspicion, not as byte-level proof
- use `protected huge hotspots` for visibility, not for blind action
- treat low-confidence findings as prompts for human judgment, not as conclusions

The selector follows a recursive dominant-space rule:

- find the children that explain about the configured dominant threshold of each branch
- keep descending while the branch stays dominant
- emit all relevant candidates from that walk, including many medium-size files when they dominate together

Dependency checks are cheap and local by default:

- heuristic signatures for cache/temp/trash/partial/system paths
- nearby reference scan for ambiguous user-owned assets
- optional broader scan only when an agent chooses to escalate on uncertain macrofolders

## Safety Rules

- never store secrets in the repository
- never change files automatically
- never issue cleanup commands from this skill
- prefer compact outputs over raw dumps
- stop loudly if the requested engine or runtime contract is wrong
- treat large user assets as review targets, not junk

## Repository Layout

- `SKILL.md`: public skill entrypoint
- `config/`: thresholds, exclusions, policy settings
- `docs/`: specs and implementation plans
- `examples/`: a real, reproducible audit demo (see [examples/README.md](examples/README.md))
- `outputs/`: generated audit runs
- `scripts/linux/`: Linux helper scripts
- `scripts/windows/`: Windows helper scripts
- `src/`: engines, parsers, classifier, reporting, CLI
- `tests/`: focused automated tests
- `.agent/`: local operator memory, ignored from git
- `trash/`: disposable experiments, ignored from git

## License

Licensed under the **Apache License 2.0** — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

