# OpenCortex Foundation Inside BMA

BMA includes the OpenCortex-style foundation as its first layer. The goal is to make BMA usable without keeping a separate `skills/opencortex/` folder.

## Core Idea

OpenCortex turns raw daily activity into structured long-term memory. BMA keeps that foundation and adds memory metabolism plus procedural learning.

## File Architecture

```text
SOUL.md          identity and personality
AGENTS.md        operating protocol and delegation rules
MEMORY.md        principles + index only
TOOLS.md         tool/API catalog
INFRA.md         infrastructure reference, optional
USER.md          human profile and communication style
BOOTSTRAP.md     session startup checklist

memory/
  projects/      per-project knowledge
  contacts/      people and organization context
  workflows/     recurring workflows and pipelines
  runbooks/      repeatable procedures
  preferences.md cross-cutting preferences
  lesson-imprint/ procedural safeguards
  archive/       downranked raw daily logs and weekly summaries
  YYYY-MM-DD.md  today's working log

memory-archive/  cold source archive for metabolized aged records
```

## Daily Distillation Role

Daily distillation remains responsible for promotion:

- project facts → `memory/projects/`
- tools and APIs → `TOOLS.md`
- infrastructure → `INFRA.md` only when enabled
- contacts → `memory/contacts/`
- workflows → `memory/workflows/`
- preferences → `memory/preferences.md`
- decisions → relevant project file or `MEMORY.md` index
- scheduled jobs → `MEMORY.md`
- failures/corrections → raw log plus Lesson-Imprint extraction

After useful information is distilled, raw logs move to `memory/archive/`.

## Weekly Synthesis Role

Weekly synthesis reviews recent archive material and structured memory for:

- recurring problems
- unfinished threads
- cross-project links
- decision capture quality
- new runbook candidates
- structural integrity
- retrieval quality
- preference/contact/workflow health

## BMA Additions

BMA adds two mechanisms on top:

1. **Retention / forgetting** for aged declarative memory.
2. **Lesson-Imprint** for procedural memory and repeated-failure safeguards.

## Attribution

BMA is inspired by and compatible with OpenCortex. OpenCortex is MIT licensed; public BMA releases should preserve upstream attribution and clearly state which pieces are derived, adapted, or reimplemented.
