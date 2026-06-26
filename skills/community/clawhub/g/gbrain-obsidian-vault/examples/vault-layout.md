# Example vault layout (after setup + export)

```
~/wiki/
├── .obsidian/              # Obsidian UI config (gitignored)
├── .gitignore
├── memory/                 # symlink → ~/.openclaw/workspace/memory/
│   ├── 2026-04-29.md
│   ├── 2026-05-07.md
│   └── ...
├── people/
│   ├── dan-koe.md
│   └── peter-thiel.md
├── companies/
│   └── deepseek.md
├── projects/
│   └── openclaw.md
├── concepts/
│   └── token-plan.md
├── synthesis/
│   └── cluster-*.md        # weekly brain-synthesis output
├── daily/                  # gbrain-ingested daily summaries
├── sessions/
└── index.md
```

## What to click in Obsidian

1. **Graph** (left ribbon) — filter by path `people` or `projects`
2. Open `concepts/token-plan.md` — see outgoing `[[projects/openclaw]]`
3. Open `memory/2026-04-29.md` — Backlinks → **Unlinked mentions** → pages citing that diary

## Typical wikilink (gbrain style)

```markdown
[[projects/openclaw]] [[people/dan-koe]]
```

## Typical memory source line (bridge without wikilink)

```markdown
[Source: memory/2026-04-29.md]
```
