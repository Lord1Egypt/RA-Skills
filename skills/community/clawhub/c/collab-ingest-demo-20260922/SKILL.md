---
name: collab-ingest-demo
description: "可复现的协作入库演示：用 workflow-structurer 把模糊流程结构化为 handoff，再按 demo-asset-ingest 规范打包，最终通过 clawhub 发布到资源中心。本资产即一次真实入库的产物，DESCRIPTION.md 为上游流程梳理结果。"
metadata:
  clawdbot:
    emoji: "📦"
    requires: ["clawhub"]
---

# Collab Ingest Demo

This asset is the real output of one end-to-end run of:

1. **workflow-structurer** — progressive clarification (goal → steps → drill-down → summary → handoff) producing a structured workflow document.
2. **demo-asset-ingest** — the packaging convention (`SKILL.md` + `references/DESCRIPTION.md`) and `clawhub publish` flow into the ClawHub resource center.

## Structure

```
collab-asset/
├── SKILL.md
└── references/
    └── DESCRIPTION.md   # upstream workflow handoff
```

## Reproduce

```bash
clawhub whoami
clawhub publish collab-asset --slug <unique-slug> --name "Collab Ingest Demo" \
  --tags "workflow,ingest,collab,demo" --topics "ingest,workflow" --dry-run
clawhub publish collab-asset --slug <unique-slug> --name "Collab Ingest Demo" \
  --tags "workflow,ingest,collab,demo" --topics "ingest,workflow"
clawhub search <unique-slug>
```
