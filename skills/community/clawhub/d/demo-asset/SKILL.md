---
name: demo-asset
description: A demo digital asset that has been processed, validated, and packaged in the OpenClaw workspace, then ingested into the ClawHub resource center to show the TaskFlow-style workflow + ClawHub CLI handoff.
metadata: {"clawdbot": {"emoji": "📦"}}
---

# Demo Asset

A minimal, self-contained digital asset that demonstrates the handoff between
two cooperating tools:

1. **Business process handling** — the OpenClaw workspace prepares, validates,
   and packages the asset into a ClawHub-skill-shaped folder.
2. **Digital resource ingest & management** — the `clawhub` CLI publishes the
   folder into the ClawHub resource center so it becomes discoverable and
   installable.

## Asset shape

```
demo-asset/
├── SKILL.md              # this file (frontmatter + prose)
└── references/
    └── DESCRIPTION.md    # supporting material produced by the workflow
```

## Reproduce the ingest

1. Preview without publishing:

   ```bash
   clawhub skill publish --dry-run demo-asset
   ```

2. Publish into the resource center:

   ```bash
   clawhub skill publish demo-asset \
     --slug demo-asset \
     --name "Demo Asset" \
     --tags "demo,ingest,workflow" \
     --topics "ingest,workflow"
   ```

3. Verify discovery:

   ```bash
   clawhub search demo-asset
   ```
