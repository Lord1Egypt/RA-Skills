# Publish / Upload Guide (ClawHub)

Skill folder:
- `/Users/victor/.openclaw/workspace/skills/context-hub-openclaw`

Published release:
- `context-hub-openclaw@0.1.0`
- Changelog: `Initial release: doc-first Context Hub workflow, annotation standards, and OpenClaw integration playbook.`

## CLI publish template

```bash
clawhub publish /Users/victor/.openclaw/workspace/skills/context-hub-openclaw \
  --slug context-hub-openclaw \
  --name "Context Hub for OpenClaw" \
  --version 0.1.0 \
  --changelog "Initial release: doc-first Context Hub workflow, annotation standards, and OpenClaw integration playbook." \
  --tags latest,context,docs,api
```

## Update flow (next version)

1. Edit `SKILL.md`
2. Bump version (semver)
3. Publish

```bash
clawhub publish /Users/victor/.openclaw/workspace/skills/context-hub-openclaw \
  --slug context-hub-openclaw \
  --name "Context Hub for OpenClaw" \
  --version 0.1.1 \
  --changelog "Add explicit OpenClaw trigger heuristics (high/medium/low confidence + 2-of-5 checklist) for when to run Context Hub before coding." \
  --tags latest,context,docs,api
```

Status: `0.1.1` is prepared locally and **not published yet**.

## Suggested listing metadata (if using web upload UI)

- **Slug:** `context-hub-openclaw`
- **Name:** `Context Hub for OpenClaw`
- **Version:** `0.1.0`
- **Summary:** `Use Context Hub (chub) for doc-first API coding in OpenClaw, with persistent annotations and version-aware fetches.`
- **Tags:** `latest, context, docs, api`
