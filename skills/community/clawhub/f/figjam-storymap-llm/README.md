# figjam-storymap-llm

> Turn a FigJam Story Map (Jeff Patton methodology) into LLM-readable Markdown / JSON — without manual transcription, without OCR hallucinations, without losing spatial semantics.

[![License: MIT](./LICENSE)](./LICENSE)

An **Agent Skill** that audits and parses FigJam User Story Maps into a deterministic Markdown / JSON output (no manual transcription, no OCR, no loss of spatial semantics) — which you can then convert into a Notion page, Linear/Jira CSV import, or paste into a coding agent (Cursor, Claude Code, Copilot) as living spec.

This is the GitHub-facing landing page. The agent-facing working document is [`SKILL.md`](./SKILL.md) — full procedure, taxonomy, quality checklist, Map Structure Guardian rules, and anti-patterns.

## Why

After a Story Mapping workshop, the team typically transcribes hundreds of sticky notes by hand into Jira / Linear. That is the worst kind of waste: workshop intent gets lost, the spatial semantics of the map are flattened, and the workshop output drifts away from what was actually agreed.

**This skill eliminates the transcription step.** It reads the FigJam board via the Figma REST API (deterministic, no OCR) and renders a structured Markdown / JSON backlog preserving:

- Activity -> Task -> User Story hierarchy (Patton backbone)
- Release slicing (V1 / V2 / V3)
- Acceptance Criteria inline with each story
- Owner and priority (V1 only — Lean UX rule)
- Connector relationships (dependencies, blockers, branching)

## Structure

```
figjam-storymap-llm/
├── SKILL.md                          # Agent-facing working document (required)
├── LICENSE                           # MIT
├── README.md                         # This file (GitHub landing page)
├── references/
│   ├── llm-ready-figjam-guidelines.md   # Condensed guidelines + industry sources
│   ├── system-prompt.md                 # System Prompt for AI agent (audit + synthesis)
│   └── figjam-template-spec.md          # Canonical FigJam template spec + checklist
└── scripts/
    └── figjam_parser.py                 # Python parser (Figma REST API -> Markdown / JSON)
```

## Quick start

### Option A — Run the parser (CLI)

```bash
pip install requests
export FIGMA_TOKEN=your_figma_personal_access_token

# Markdown output
python scripts/figjam_parser.py \
  --file-key {YOUR_FILE_KEY} \
  --token $FIGMA_TOKEN > story-map.md

# JSON output for PM tooling import
python scripts/figjam_parser.py \
  --file-key {YOUR_FILE_KEY} \
  --token $FIGMA_TOKEN --format json > story-map.json

# Offline mode (use a saved Figma JSON export instead of calling the API)
python scripts/figjam_parser.py --input saved-board.json > story-map.md
```

### Option B — Use as an Agent Skill

Copy this folder into your `.agents/skills/` directory (or `.claude/skills/` for Claude Code). Then load it on demand:

- **Claude Code CLI:** tell Claude "load the figjam-storymap-llm skill and audit my FigJam board"
- **Cursor / Copilot:** paste `SKILL.md` + `references/system-prompt.md` as project context

### Option C — Audit a board (no parsing)

Paste the `references/system-prompt.md` content as System Instructions, then share a screenshot of your FigJam board (or JSON). The agent returns an LLM-readiness audit.

### Option D — Start from the published FigJam template

A ready-to-use FigJam Story Map template built to this spec is published on Figma Community:

**[LLM Story Map — AI-readable User Story Map template](https://www.figma.com/community/file/1661156551667594442)**

Duplicate it, replace `[PRODUCT NAME]` in the AI Readme, fill the backbone with your Activities / Tasks, and the parser reads it out of the box.

## What's inside `SKILL.md`

The full procedure covers:

- **Workflow** (5 steps): gather input -> audit LLM-readiness -> run parser -> verify output -> convert to PM tooling
- **Taxonomy** of sticky tags (`[STORY]`, `[V1]`, `[P1]`, `@DEV`, `[ACT_*]`, `[TASK_*]`, `Acceptance Criteria:`)
- **Quality Checklist** (8 items) for declaring a board LLM-ready
- **Map Structure Guardian** — active coach enforcing Patton + Cohn INVEST rules (not a passive reader)
- **Anti-patterns** (9 items) — manual IDs on stories, AC on separate stickies, priorities in V2/V3, connectors for linear flow, etc.
- **Framework Credits** — Patton, Gothelf & Seiden (Lean UX), Torres, Ries, Cohn

## Methodology

This skill adapts and combines:

- **Jeff Patton — User Story Mapping** (O'Reilly, 2014) — Backbone + Slices + Walking Skeleton
- **Gothelf & Seiden — Lean UX** (2013) — Hypothesis-driven, no Big Upfront Design in V2 / V3
- **Mike Cohn — User Stories Applied** (2004) — INVEST, AC inline
- **Teresa Torres — Continuous Discovery Habits** (2023) — Story Map as living artifact
- **Figma REST API** — Node types (SECTION, STICKY, SHAPE_WITH_TEXT, CONNECTOR)
- **Anthropic Vision Guidelines** — Layout & spatial data in Vision LLM prompts

Full source list in `references/llm-ready-figjam-guidelines.md`.

## Industry references

- Figma REST API: https://www.figma.com/developers/api
- Anthropic Vision: https://docs.anthropic.com/en/docs/build-with-claude/vision
- tldraw (canvas-to-JSON reference): https://github.com/tldraw/tldraw
- Jeff Patton — User Story Mapping: https://www.jpattonassociates.com/user-story-mapping/

## License

MIT — see [`LICENSE`](./LICENSE).

## Trademarks

FigJam and Figma are registered trademarks of Figma, Inc. This project is an independent open-source tool and is not affiliated with, endorsed by, or sponsored by Figma, Inc. The name "figjam" in the repository and skill identifiers is used for nominative fair use — to describe compatibility with the FigJam platform.