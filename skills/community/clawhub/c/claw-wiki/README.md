# Claw Wiki

`claw-wiki` is an OpenClaw skill repository that keeps a local, searchable snapshot of the OpenClaw documentation.

It is designed for two jobs:

- Answer OpenClaw questions from checked-in docs instead of model memory
- Refresh that snapshot from the upstream OpenClaw repository in a repeatable way

The repository combines an OpenClaw skill entrypoint (`SKILL.md`), a local docs corpus (`openclaw_docs/`), and maintenance scripts for syncing, validating, indexing, and diffing updates.

In practice, this repo works best as an OpenClaw knowledge skill that you install into a workspace or shared skill directory, then let OpenClaw load into sessions when documentation lookup or docs maintenance is needed.

## What is in this repo

- `SKILL.md`: the OpenClaw skill definition and lookup workflow
- `openclaw_docs/`: the current local OpenClaw docs snapshot
- `docs.json`: docs navigation metadata copied from upstream
- `references/`: routing, query, and update helpers used by the skill
- `scripts/`: sync and validation utilities
- `state/`: generated metadata about the current snapshot

## Typical use cases

- You want a local OpenClaw reference corpus that OpenClaw can load and cite by file path
- You want deterministic answers based on a pinned docs snapshot
- You want to check whether your local OpenClaw docs are stale
- You want to pull the latest upstream docs and generate a change summary

## Install as an OpenClaw skill

OpenClaw can load skills from your workspace `./skills` directory or from `~/.openclaw/skills`. Clone or copy this repo into one of those locations and keep the folder name as `claw-wiki`.

Example:

```bash
git clone https://github.com/lueashes/claw-wiki.git
cp -R claw-wiki ~/.openclaw/skills/claw-wiki
```

Workspace-local installation is also valid:

```bash
git clone https://github.com/lueashes/claw-wiki.git ./skills/claw-wiki
```

After that, OpenClaw can load the skill when the task is clearly about OpenClaw docs lookup or docs refresh.

## How it fits into OpenClaw

OpenClaw skill precedence is:

`<workspace>/skills` -> `~/.openclaw/skills` -> bundled skills

That makes `claw-wiki` useful in two common modes:

- Workspace skill: keep it inside one project or one OpenClaw agent workspace
- Shared skill: install once in `~/.openclaw/skills` and reuse it across agents on the same machine

If you later want to distribute it more broadly, this repo also matches the normal OpenClaw skill bundle structure used by ClawHub.

## How the skill works

The skill answers questions from local files under `openclaw_docs/`, then cites exact paths used to produce the answer.

The normal lookup flow is:

1. Route the question to likely docs areas with `references/routing-cheatsheet.md`
2. Narrow candidates with `rg --files` or `rg -n`
3. Read the top relevant docs files in full
4. Answer with explicit file-path citations

For freshness-sensitive questions, the skill also reads:

- `state/source-lock.json` for the upstream source, ref, commit, and sync timestamp
- `state/latest-diff.md` for the last snapshot diff summary

## Repository layout

```text
claw-wiki/
├── SKILL.md
├── README.md
├── docs.json
├── openclaw_docs/
├── references/
│   ├── query-examples.md
│   ├── routing-cheatsheet.md
│   └── update-workflow.md
├── scripts/
│   ├── build_knowledge.py
│   ├── diff_docs.py
│   ├── sync_docs.py
│   └── validate_docs.py
└── state/
    ├── docs-manifest.json
    ├── latest-diff.md
    ├── source-lock.json
    └── topic-index.json
```

## Refresh the OpenClaw docs snapshot

This repo is meant to mirror the upstream OpenClaw docs into `openclaw_docs/`.

### Option 1: Sync from a local OpenClaw checkout

Use this when you already have the upstream repo on disk.

```bash
python scripts/sync_docs.py --source-path ../openclaw --mode pinned
python scripts/validate_docs.py
python scripts/build_knowledge.py
python scripts/diff_docs.py
```

### Option 2: Sync from GitHub

Use this when you want to refresh directly from upstream.

```bash
python scripts/sync_docs.py --repo-url https://github.com/openclaw/openclaw --ref main --mode tracking
python scripts/validate_docs.py
python scripts/build_knowledge.py
python scripts/diff_docs.py
```

## What the maintenance scripts do

- `scripts/sync_docs.py`: copies docs and `docs.json` from upstream into this repo and records snapshot metadata
- `scripts/validate_docs.py`: checks that required doc areas exist and `docs.json` does not reference missing pages
- `scripts/build_knowledge.py`: builds `state/docs-manifest.json`, `state/topic-index.json`, and a generated routing cheatsheet
- `scripts/diff_docs.py`: compares the previous and current manifests and writes `state/latest-diff.md`

## Snapshot metadata

The current snapshot state is tracked in committed files under `state/`.

The most important one is `state/source-lock.json`, which records:

- upstream repository URL
- tracked ref
- resolved upstream commit
- sync timestamp
- whether the snapshot came from a local repo or a fresh clone

This makes it possible to answer version-sensitive questions without guessing.

## Requirements

- Python 3.10+ is sufficient for the included scripts
- `git` is required for remote sync mode
- `rg` is recommended for fast lookup during interactive use

The maintenance scripts use only the Python standard library.

## Usage notes

- The checked-in snapshot currently targets the English OpenClaw docs set
- Generated files under `state/` should be rebuilt after every sync
- Validation should pass before you claim a refresh succeeded
- This repo is intended for OpenClaw-local reference and maintenance workflows, not for pushing changes back into the upstream OpenClaw docs repo

## ClawHub positioning

This repository is structured so it can function as:

- a directly cloned OpenClaw skill in `./skills` or `~/.openclaw/skills`
- a future ClawHub-published skill bundle for OpenClaw users

If you publish it through ClawHub later, the core behavior should stay the same: OpenClaw loads `SKILL.md`, uses the bundled docs snapshot, and relies on the included scripts to refresh and validate the knowledge base.

## Related files

- [`SKILL.md`](./SKILL.md)
- [`references/update-workflow.md`](./references/update-workflow.md)
- [`state/source-lock.json`](./state/source-lock.json)
- [`state/latest-diff.md`](./state/latest-diff.md)
