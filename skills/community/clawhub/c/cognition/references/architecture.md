# Cognition — Architecture Notes

Use this file when you need the fuller operating model behind the lean `SKILL.md` entrypoint.

## 1) Core systems

### Daily memory
`memory/YYYY-MM-DD.md`

Use daily logs as append-only session memory and source material for later consolidation.

### Durable knowledge
`MEMORY.md` + `memory/bank/*.md`

Keep `MEMORY.md` short and navigational. Put deeper project, user, domain, or system detail in `memory/bank/` files.

### Commitments
`memory/FUTURE_INTENTS.md`

Use this for future actions, reminders, triggers, and deferred work so commitments do not disappear between sessions.

### Procedures
`memory/procedures/` + `memory/procedures/index.yaml`

Promote solved workflows into reusable procedures. Default all new procedures to `draft` until they are reviewed or repeatedly validated.

## 2) Recommended operating model

### Broadcast important information deliberately
Treat this as protocol, not a new subsystem:
- new preference → durable knowledge
- new commitment → `memory/FUTURE_INTENTS.md`
- novel solution → procedures
- correction → fix the durable record and note the lesson
- failed retrieval → `memory/meta/gap_tracker.json`

### Safe consolidation
Before any reviewed workflow mutates durable memory:
1. back up the target file(s)
2. stage proposals first
3. preserve provenance
4. tag uncertain items `[NEEDS_REVIEW]`

Daily logs remain append-only source material. Consolidation should not rewrite or compress them.

### Procedure maturity
- `draft` — new or lightly proven
- `reviewed` — human-reviewed or proven by 3 successful executions
- `trusted` — repeatedly validated with no unresolved caveats

## 3) Advanced overlays

These are optional. Do not adopt them before the core system is already being used.

### Cross-references
`memory/bank/cross-references.md`

Use this to link adjacent people, projects, and files so retrieval can branch outward when needed.

### Confidence tracking
`memory/KNOWLEDGE_MAP.md`

Use coarse confidence bands:
- 🟢 high
- 🟡 medium
- 🔴 low

Prefer `last_verified` dates over fake precision.

### Gap tracking
`memory/meta/gap_tracker.json`

Use this for repeated misses, missing docs, recurring uncertainty, or retrieval blind spots.

### Retrieval logging
`memory/meta/retrieval_log.json`

Use this only if you actually review retrieval quality over time.

## 4) Retrieval tiers

### Tier 0 — Manual
Use naming conventions, `rg`, and deliberate file structure.

### Tier 1 — Keyword search
Use text search or memory search over daily logs and bank files.

### Tier 2 — Hybrid retrieval
Use embeddings + keyword search + ranking if your environment supports it.

The settings in `references/config.md` are Tier 2 guidance only. They are optional, not part of baseline adoption.

## 5) File structure

```text
workspace/
├── MEMORY.md
└── memory/
    ├── FUTURE_INTENTS.md
    ├── KNOWLEDGE_MAP.md              # optional Advanced overlay
    ├── YYYY-MM-DD.md
    ├── bank/
    │   └── cross-references.md       # optional Advanced overlay
    ├── consolidation/
    │   └── YYYY-MM-DD-staged.md
    ├── meta/
    │   ├── gap_tracker.json
    │   └── retrieval_log.json
    ├── procedures/
    │   └── index.yaml
    └── summaries/
        └── YYYY-WNN.md
```

## 6) What not to do

- do not silently mutate durable files during consolidation
- do not let `MEMORY.md` become a raw archive
- do not treat optional overlays as mandatory architecture
- do not promote procedures just because they sound useful
- do not fake certainty when retrieval fails
