# ClawHub Publisher

CLI-first tool for turning local OpenClaw skills into cleaner, publish-ready ClawHub packages.

This repo also ships a root `SKILL.md`, so the project can publish itself as proof that the workflow works in practice.

## What improved in v0.1.1

- clearer validation summaries with errors, warnings, info counts, and actionable hints
- better detection for common packaging mistakes:
  - missing or broken `SKILL.md`
  - missing `name` / `description`
  - weakly short descriptions
  - missing `README`
  - blank hook files
  - frontmatter hook paths pointing to missing files
  - absolute hook paths that should be relative
- richer prepare output with copied/removed counts and cleaner report data
- safer publish UX:
  - semver validation for `--skill-version`
  - required changelog in non-interactive mode
  - final publish confirmation unless `--yes` is used
- clearer built-in help and better examples

## Why this exists

Publishing OpenClaw skills manually works, but small packaging mistakes are easy to miss:

- a missing `SKILL.md`
- invalid YAML frontmatter
- metadata that is technically valid but weak for discovery
- hook references that point to files that do not exist
- blank files that make the package feel sloppy
- noisy local folders that should never be bundled

ClawHub Publisher gives you a repeatable pre-publish pipeline instead of a one-off manual checklist.

## Requirements

- Node.js 20+
- npm
- optional for the final publish step: `clawhub` CLI

Install ClawHub CLI if you want to publish directly:

```bash
npm i -g clawhub
```

## Install

```bash
npm install
```

## Build

```bash
npm run build
```

## Use the built CLI

```bash
node dist/index.js --help
```

## Commands

### Validate a skill

```bash
node dist/index.js validate "/path/to/my-skill"
```

What you get now:

- total files scanned
- error / warning / info counts
- hook, docs, binary, and empty-file stats
- clearer issue messages with hints
- a clean “ready to prepare/publish” outcome when applicable

### Prepare a cleaned publish bundle

```bash
node dist/index.js prepare "/path/to/my-skill" --zip
```

Output is written under:

```text
.clawhub-publisher/<slug>
```

Optional zip export:

```text
.clawhub-publisher/<slug>.zip
```

Each prepared bundle also includes:

```text
publish-report.json
```

The report now includes:

- copied file count
- removed file count
- severity counts
- validation issues
- extracted metadata
- practical recommendations

### Publish with guidance

Interactive:

```bash
node dist/index.js publish "/path/to/my-skill"
```

Non-interactive:

```bash
node dist/index.js publish "/path/to/my-skill" \
  --no-prompt \
  --slug my-skill \
  --name "My Skill" \
  --skill-version 0.1.1 \
  --changelog "Polished validation and publish UX" \
  --tags latest \
  --yes
```

Notes:

- `--skill-version` must be valid semver
- `--changelog` is required in non-interactive publish mode
- publish asks for a final confirmation unless `--yes` is used
- `--dry-run` shows the exact `clawhub publish` command without executing it

### Interactive wizard

```bash
node dist/index.js wizard
```

## Demo fixture

A small skill fixture is included at:

```text
examples/demo-skill
```

Try it:

```bash
node dist/index.js validate examples/demo-skill
node dist/index.js prepare examples/demo-skill --zip
```

The fixture intentionally includes a blank hook file so validation and cleanup are easy to see.

## Example workflow

```bash
npm run build
node dist/index.js validate examples/demo-skill
node dist/index.js prepare examples/demo-skill --zip
node dist/index.js publish . \
  --no-prompt \
  --slug clawhub-publisher-cli \
  --name "ClawHub Publisher" \
  --skill-version 0.1.1 \
  --changelog "Improved validation, reports, docs, and publish safety" \
  --tags latest \
  --yes
```

## Current limits

This is still deliberately practical, not a full registry schema validator.

- validation is heuristic
- publish auth still relies on `clawhub login`
- no GUI yet
- no batch multi-skill dashboard yet

## Good next steps after this release

1. stricter schema-aware validation
2. preview diff for prepared output
3. semantic version bump helpers
4. saved publish profiles
5. batch publish queue
6. a local UI or Electron wrapper

## License

MIT
