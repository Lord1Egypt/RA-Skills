---
name: asset-ingest-guide
description: Reference skill demonstrating TaskFlow + ClawHub tooling for publishing digital content to the resource hub.
metadata:
  {
    "openclaw": {
      "emoji": "📦",
      "controller": "asset-ingest-guide",
      "purpose": "sample-resource",
    },
  }
---

# Asset Ingest Guide (demo resource)

This skill is a minimal reference artifact: a placeholder "digital content" file
that was prepared with a TaskFlow workflow and then uploaded to the ClawHub
resource center using the `clawhub publish` command.

## Purpose

- Provide a repeatable demo: business process (TaskFlow) + digital asset
  management (ClawHub).
- Demonstrate the smallest viable skill folder shape for new contributors.

## Shape

```
skills/asset-ingest-guide/
├── SKILL.md          # this file (frontmatter + prose)
└── references/       # optional supporting files
```

## Use

1. Read `SKILL.md` frontmatter for metadata.
2. Follow the orchestration guide that ships alongside (normally in the
   workspace root, e.g. `ASSET-INGEST-WORKFLOW.md`) to reproduce the full
   prepare → validate → publish → verify pipeline.
