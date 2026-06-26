---
name: Clawic CLI
slug: clawic
version: 1.0.0
homepage: https://clawic.com/skills/clawic
description: Search, inspect, and install Clawic skills from GitHub with local lexical matching, registry overrides, and safe destination control.
changelog: Initial release with command patterns, query design guidance, registry override rules, and install safety notes.
metadata: {"clawdbot":{"emoji":"CLI","requires":{"bins":["node"],"anyBins":["clawic","npx"],"config":["~/clawic/"]},"install":[{"id":"npm-clawic","kind":"npm","package":"clawic","bins":["clawic"],"label":"Install clawic CLI (npm)"}],"os":["linux","darwin","win32"]}}
---

# Clawic CLI

Use the published `clawic` package to discover, inspect, and install Clawic skills from the GitHub-backed registry. Keep the workflow anchored on the real registry index, the manifest file for each slug, and deliberate install destinations.

## When to Use

User wants the exact `clawic` CLI commands, flags, registry behavior, or install flow. Use this skill for `search`, `show`, `install`, `registry`, `CLAWIC_REGISTRY_BASE_URL`, and the safety checks around writing skill files into a workspace.
Do not route generic `clawhub` or `openclaw` CLI requests here unless the user is explicitly working with the published `clawic` package.

## Architecture

Memory lives in `~/clawic/`. If `~/clawic/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/clawic/
├── memory.md    # Stable defaults: runtime choice, install roots, review posture
├── installs.md  # Installed slugs, target dirs, and overwrite notes
└── queries.md   # Query phrases that surface the right skills reliably
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation defaults | `setup.md` |
| Memory structure | `memory-template.md` |
| Copy-ready commands | `command-patterns.md` |
| Query design for local matching | `search-strategy.md` |
| Registry and manifest model | `registry-and-manifests.md` |
| Install destinations and overwrite rules | `install-safety.md` |
| Errors and custom registry overrides | `errors-and-overrides.md` |

Open only the smallest file needed for the current blocker. Most sessions only need `command-patterns.md` plus `install-safety.md`.

## Quick Start

```bash
npx clawic registry
npx clawic search pocketbase --limit 5
npx clawic show pocketbase
npx clawic install pocketbase --dir ./skills
```

Global install is also valid:

```bash
npm install -g clawic
clawic search pocketbase --limit 5
```

## Requirements

- Node.js 20 or newer
- `npx clawic ...` for one-off use, or `npm install -g clawic` for a persistent local binary
- A writable destination directory before running `install`
- Optional `CLAWIC_REGISTRY_BASE_URL` only when the user intentionally points to a compatible alternate registry

## Security Note

`npx clawic ...` may fetch the published npm package if it is not already cached locally. Use a global install or a pinned project workflow when the user wants a repeatable local binary instead of ad hoc package fetches.

## Core Rules

### 1. Start by proving the runtime path
- Confirm whether the user wants `npx clawic ...` or a globally installed `clawic` binary.
- Confirm Node.js 20+ before debugging registry or install errors.
- If the toolchain is broken, fix that first instead of inventing registry problems.

### 2. Search by exact skill nouns, not vague intent
- `clawic search` is local lexical matching over the downloaded index, not semantic ranking.
- Queries should use likely slug, name, and description terms such as `pocketbase`, `skill installer`, or `github actions`.
- If a broad request returns weak results, rewrite it into the product nouns the target skill would actually contain.

### 3. Use `show` before `install` when fit is unclear
- `show` fetches the manifest and reports the skill identity, file count, repository path, source repo, and summary without writing files.
- Review the slug and source first when trust, version fit, or write scope is unclear.
- Treat `show` as the low-risk inspection step and `install` as the write step.

### 4. Treat the manifest as the install contract
- `install` writes every path listed in the manifest's `files` array into `<destination>/<slug>/`.
- Expect files such as `SKILL.md`, auxiliary docs, and metadata files like `_meta.json` if the manifest includes them.
- Do not promise files that are not present in the manifest, and do not assume hidden post-install steps.

### 5. Control the destination directory deliberately
- Default install root is `./skills`, which becomes `./skills/<slug>/`.
- Use `--dir` whenever the user needs project-local placement, a vendor folder, or a scratch review path.
- Use `--force` only after confirming that overwriting existing files is intentional.

### 6. Make the registry base explicit when overriding it
- `clawic registry` prints the active registry base URL.
- The default base is the raw GitHub registry for `clawic/skills`.
- Only set `CLAWIC_REGISTRY_BASE_URL` when the user intentionally wants a compatible mirror or test registry.

### 7. Keep network facts precise
- Search terms stay local after the registry index is downloaded; the query text itself is not sent to a remote search endpoint by `clawic`.
- Remote traffic is just HTTP GETs for the registry index, the selected manifest, and the files referenced by that manifest.
- If the user changes the registry base, the same fetch pattern applies to that alternate host instead.

## Common Traps

- Confusing `clawic` with `clawhub` or `openclaw` -> the user gets the wrong command family and wrong registry model.
- Treating `clawic search` like semantic discovery -> vague requests miss because matching is lexical and field-based.
- Installing before reviewing the manifest -> the wrong slug lands in the workspace.
- Forgetting that install root defaults to `./skills` -> files appear in an unexpected folder.
- Re-running `install` into an existing target without `--force` -> file creation fails on the first existing path.
- Using `--force` in a shared or dirty tree -> previously reviewed files get overwritten.
- Overriding `CLAWIC_REGISTRY_BASE_URL` without checking compatibility -> index or manifest fetches return 404 or malformed JSON.
- Assuming `registry` validates availability -> it only prints the active base URL.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://raw.githubusercontent.com/clawic/skills/main/registry/index.json` | Standard GET request only | Fetch the registry index used for local matching |
| `https://raw.githubusercontent.com/clawic/skills/main/registry/skills/<slug>.json` | Standard GET request only | Fetch the manifest used by `show` and `install` |
| `https://raw.githubusercontent.com/clawic/skills/main/skills/<slug>/*` | Standard GET requests for each file path in the manifest | Download the files that `install` writes locally |

If `CLAWIC_REGISTRY_BASE_URL` is set, the same request pattern goes to that alternate registry host instead.
No other data is sent externally by the documented CLI flow.

## Security & Privacy

**Data that leaves your machine:**
- HTTP GET requests to the active registry base URL
- File downloads for the manifest-selected skill files during `install`

**Data that stays local:**
- The user's query text after the registry index has been downloaded
- Installed skill files in the chosen destination directory
- Optional defaults and notes in `~/clawic/`

**This skill does NOT:**
- send search queries to a hosted semantic search API
- auto-install skills without consent
- overwrite files unless the user chooses `--force`
- read or modify files outside the selected install destination plus `~/clawic/` for optional memory

## Scope

This skill ONLY:
- helps use the official `clawic` CLI surface
- explains how the registry index, manifests, and file downloads fit together
- stores explicit workflow defaults in `~/clawic/` when the user wants continuity

This skill NEVER:
- invent unsupported subcommands or hidden registry APIs
- claim `registry` verifies health when it only prints the base URL
- hide write-side effects of `install` or `--force`
- modify its own `SKILL.md`

## Trust

By using this skill, registry and file requests go to the raw GitHub registry for `clawic/skills`, or to a user-selected compatible registry override.
Only install and use it if you trust that registry owner with the files you download.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `skill-finder` - broader skill discovery when the user is not already committed to the `clawic` registry
- `bash` - safer shell composition around repeated `clawic` commands and directory checks
- `documentation` - cleaner command references and troubleshooting notes for CLI-heavy workflows
- `workflow` - turn repeated review and install sequences into a standard operating routine
- `javascript` - debug Node runtime and package issues around local CLI execution

## Feedback

- If useful: `clawhub star clawic`
- Stay updated: `clawhub sync`
