# clawsqlite-knowledge Skill

## What This Skill Is

`clawsqlite-knowledge` is a thin OpenClaw/ClawHub skill wrapper around the
published `clawsqlite` PyPI package.

Installing this skill from ClawHub installs only the wrapper. Run
`bootstrap_deps.sh` before using the CLI. In managed Python environments the
global `clawsqlite` command may not appear on `PATH`; use the stable local
entry `bin/clawsqlite`.

It exists to help agents call the official `clawsqlite knowledge ...` CLI
consistently from a fixed knowledge instance home.

## Relationship To clawsqlite

This skill does not implement knowledge-base logic. The implementation lives in
the upstream `clawsqlite` package and its official CLI.

This skill intentionally does not:

- vendor the `clawsqlite` source tree
- clone the GitHub repository
- add a `run_clawknowledge.py` runtime wrapper
- define a second JSON API
- maintain a second configuration system

## Installation

Install the skill shell into the workspace, then run:

```bash
sh bootstrap_deps.sh
```

The bootstrap script first checks Python 3.10+, importability, and the pinned
`clawsqlite==1.0.12` package contract. It installs only when that contract is not
already satisfied, then validates the stable local entry:

```bash
./bin/clawsqlite
```

## Configuration

Create or edit the local private config in a knowledge instance home, not in
the skill directory:

```bash
./bin/clawsqlite knowledge maintenance init-config --instance default
cd ~/.openclaw/workspace/data/clawsqlite-knowledge/default
```

In OpenClaw, the default instance home is under the persistent workspace data
directory. On ordinary non-OpenClaw Linux installs it falls back to
`${XDG_DATA_HOME:-~/.local/share}/clawsqlite-knowledge/default`.

`clawsqlite.toml` is the single runtime configuration source. This skill does
not include an env example because normal operation should not use environment
variables as a second config layer.

## Validate With Doctor

```bash
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge maintenance doctor --json
```

## Common Commands

```bash
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record ingest --url "https://example.com/post" --category web_article --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record ingest --text "some note" --title "Saved note" --category note --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record search "vector database design" --mode hybrid --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge record show --id 123 --full --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge maintenance cleanup --days 3 --dry-run --json
<workspace>/skills/clawsqlite-knowledge/bin/clawsqlite knowledge maintenance backup --dry-run --json
```

For text ingest, `--title` is a `source_title` hint for archive filenames and
metadata. Strict ingest stores the LLM-produced knowledge title in
`generated_title`.

## When To Use clawsqlite Directly

Use `clawsqlite` directly whenever you are developing or debugging the upstream
package itself. Use this skill when an Agent needs a small, stable instruction
surface for operating a configured knowledge instance.
