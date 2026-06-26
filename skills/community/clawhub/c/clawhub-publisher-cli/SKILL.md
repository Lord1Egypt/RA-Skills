---
name: clawhub-publisher
description: Use the bundled ClawHub Publisher CLI to validate, prepare, zip, and publish OpenClaw skills to ClawHub with clearer validation, cleaner packaging, and safer publish prompts.
---

# ClawHub Publisher

Use this skill when you need to turn a local OpenClaw skill folder into a publish-ready ClawHub package.

This repository also ships the matching CLI implementation used by the skill, and the project is intentionally self-publishable.

## What it does

- validates a skill folder before publish
- detects common blockers like:
  - missing `SKILL.md`
  - broken YAML frontmatter
  - missing `name` / `description`
  - missing `README`
  - blank hook files
  - hook references that point to missing files
- prepares a cleaned publish-ready output bundle
- optionally exports a zip archive
- runs the final `clawhub publish` command with explicit metadata
- asks for final confirmation before publishing unless you pass `--yes`

## Preferred workflow

From the project root:

```bash
npm install
npm run build
```

Use the built CLI:

```bash
node dist/index.js validate "/path/to/skill"
node dist/index.js prepare "/path/to/skill" --zip
node dist/index.js publish "/path/to/skill"
```

## Fast non-interactive publish example

```bash
node dist/index.js publish "/path/to/skill" \
  --no-prompt \
  --slug my-skill \
  --name "My Skill" \
  --skill-version 0.1.1 \
  --changelog "Polished validation and publish UX" \
  --tags latest \
  --yes
```

## Notes

- `clawhub` CLI login is still required for the final publish step.
- prepared output is written under `.clawhub-publisher/`
- the source skill folder is left untouched
