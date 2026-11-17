---
name: demo-asset-ingest
description: Demonstrates the end-to-end collaboration between a business process workflow (TaskFlow-style workspace orchestration) and a digital asset management tool (ClawHub CLI) — from preparing a publishable artifact to ingesting it into the ClawHub resource center.
metadata: {"clawdbot":{"emoji":"📦","requires":["clawhub"],"homepage":"https://clawhub.ai"}}
---

# Demo Asset Ingest

A minimal, reusable demo showing how two cooperating tools work together:

1. **Business process handling**: Use the OpenClaw workspace to prepare, validate, and package a digital asset into a ClawHub-skill-shaped folder.
2. **Digital asset ingestion & management**: Use the `clawhub` CLI to publish the folder as a skill in the ClawHub resource center, making it discoverable and installable.

## When to use this

- You need a repeatable pattern for "process content → publish into a resource center".
- You want to teach or demo how TaskFlow-style orchestration and ClawHub publishing collaborate.
- You are authoring a new skill and want the smallest viable shape to start with.

## Asset shape

```
demo-asset/
├── SKILL.md              # this file (frontmatter + prose)
└── references/
    └── DESCRIPTION.md    # supporting material produced by the upstream workflow
```

## End-to-end usage (quick start)

1. **Process the asset** in the workspace (TaskFlow-style):
   - Create the folder layout and content above.
   - Validate locally: `ls -R demo-asset`.

2. **Ingest into the resource center** with the ClawHub CLI:
   - Preview: `clawhub skill publish --dry-run demo-asset`
   - Publish: `clawhub skill publish demo-asset --slug demo-asset-ingest --name "Demo Asset Ingest" --tags "demo,ingest,workflow" --topics "ingest,workflow"`

3. **Verify**: `clawhub search demo-asset-ingest` (allow for moderation if newly published).
