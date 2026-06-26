---
name: elite-to-expertpack
description: "Convert Elite Longterm Memory data into a structured ExpertPack. Migrates the 5-layer memory system (SESSION-STATE hot RAM, LanceDB warm store, Git-Notes cold store, MEMORY.md curated archive, and daily journals) into ExpertPack's portable format with multi-layer retrieval, context tiers, and EK measurement. Output is Obsidian-compatible — includes YAML frontmatter on all content files and can be opened as an Obsidian vault. Use when: upgrading from Elite Longterm Memory to ExpertPack, backing up agent knowledge, or migrating to a new platform. Triggers on: 'elite to expertpack', 'convert elite memory', 'export elite memory', 'migrate elite longterm', 'upgrade memory to expertpack', 'elite memory export'."
metadata:
  openclaw:
    homepage: https://expertpack.ai
    requires:
      bins:
        - python3
---

# Elite Longterm Memory → ExpertPack

Converts an **Elite Longterm Memory** (5-layer system with 32K ClawHub downloads) into a proper structured **ExpertPack**.

**Supported layers:**

- **Hot RAM** — `SESSION-STATE.md` (current task, context, decisions)
- **Warm Store** — LanceDB vectors at `~/.openclaw/memory/lancedb/` (note: exported or skipped)
- **Cold Store** — Git-Notes JSONL (decisions, learnings, preferences)
- **Curated Archive** — `MEMORY.md`, `memory/YYYY-MM-DD.md` journals, `memory/topics/*.md`
- **Cloud** — SuperMemory/Mem0 (skipped, noted in overview)

## Usage

```bash
cd /root/.openclaw/workspace/ExpertPack/skills/elite-to-expertpack
python3 scripts/convert.py \
  --workspace /path/to/your/workspace \
  --output ~/expertpacks/my-agent-pack \
  [--name "My Agent's Knowledge"] \
  [--type auto|person|agent]
```

Flags let you override auto-detected paths for each layer.

## What It Produces

A complete ExpertPack conforming to schema 2.3:

- `manifest.yaml` (with context tiers, EK stub)
- `overview.md` summarizing conversion (layer counts, warnings)
- Structured directories: `mind/`, `facts/`, `summaries/`, `operational/`, `relationships/`, etc.
- `_index.md` files, lead summaries, `glossary.md` (if terms found)
- `relations.yaml` (if relationships detected)
- Clean deduplication preferring curated > structured > raw sources

**Secrets are automatically stripped** (sk-*, ghp_*, tokens, passwords). Warnings emitted for any found.

## Post-Conversion Steps

1. `cd ~/expertpacks/my-agent-pack`
2. Verify content files are 400–800 tokens each (Schema 2.5 — retrieval-ready by design)
3. Measure EK ratio: `python3 /path/to/expertpack/tools/eval-ek.py .`
4. Review `overview.md` and `manifest.yaml`
5. Commit to git and publish to ClawHub

**Learn more:** https://expertpack.ai • ClawHub [expertpack skill](https://clawhub.com/skills/expertpack)

**See also:** Elite Longterm Memory skill on ClawHub.
