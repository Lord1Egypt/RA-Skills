---
created: 2026-07-20
updated: 2026-07-20
version: 1.1
description: Executive Summary of the figjam-storymap-llm skill for the FigJam canvas. Human-facing cover page that points to ClawHub (install) and GitHub (source).
---

# FigJam Story Map — Executive Summary (canvas cover page)

Insert at the top of the canvas (or as the first text block inside `[00_SECTION_AI_Readme]` visible to humans). This is the human-facing summary; the full System Instructions for the AI agent live in `figjam-template-spec.md` (section `[00_SECTION_AI_Readme]`).

```text
System Instructions for AI Parser

This template turns a FigJam Story Map (Jeff Patton methodology) into
LLM-readable Markdown / JSON — no manual transcription, no OCR, no loss
of spatial semantics. The parser reads the board via Figma REST API and
renders a structured Markdown / JSON output — no information loss, with
legend, following industry best practices (Patton, Cohn, Lean UX).

What makes this board LLM-ready

- [STORY_MAP] root wraps the whole canvas — zero unsectioned stickies
- Sections tagged with deterministic prefixes ([03_SECTION_Release_1], ...)
- Sticky taxonomy in square brackets: [STORY] [V1] [P1] sentence @DEV
- Acceptance Criteria inline in the story sticky (NOT a separate sticky)
- V1 with full taxonomy (priority + owner); V2 / V3 clean (Lean UX)
- Chronology encoded in X axis; stories mapped to tasks algorithmically
- Connectors only for branching / cross-release dependencies
- [00_SECTION_AI_Readme] on canvas = the agent's operating manual

How to use this board

Fill the backbone: [ACT_*] and [TASK_*] in user voice (not build voice)
Slice releases: V1 walking skeleton, V2 / V3 hypotheses (clean)
Write stories: [STORY] [V1] [P1] sentence @DEV + Acceptance Criteria
Run the parser (CLI or agent) — get Markdown / JSON backlog
Paste into a coding agent
and optionally push to Notion / Linear / Jira through MCP/CSV

Get the skill + parser

ClawHub (one-click install):
https://clawhub.ai/monikazapisekstudio/skills/figjam-storymap-llm

GitHub (source code, parser, full spec):
github.com/monikazapisek/design-engineering-playbook/tree/main/skills/figjam-storymap-llm

CLI parser (after cloning):
python scripts/figjam_parser.py --file-key {KEY} --token $FIGMA_TOKEN

MIT licence — free to use, fork, and ship.

Recommended Reading
This Story Map template & skill integrates the following world-class
agile methodologies:

User Story Mapping (Jeff Patton): The core 2D structure (Horizontal
Sequence / Vertical Slices) is based on Patton's technique for building
shared understanding and visualizing the 'Walking Skeleton'.

Better User Stories (Mike Cohn): The hierarchy of Activities, Tasks,
and Stories, along with the 'Significant Objective' framing, follows
Cohn's strategic approach to backlog refinement.

Continuous Discovery Habits (Teresa Torres): The 'Problem Framing' and
'Strategic Context' placeholders ensure that the map remains aligned
with validated user opportunities and business outcomes.

Escaping the Build Trap (Melissa Perri): The release strategy (V1-V3)
is designed to prioritize validated value over simple output, ensuring
the team solves real business problems.

Lean UX (Jeff Gothelf & Josh Seiden): The inclusion of 'Core Value Proof'
in V1 reflects the hypothesis-driven approach to product design.
```

## Where to put this on the canvas

- As a single TEXT node at the top of `[00_SECTION_AI_Readme]` (above the full System Instructions block), OR
- As a separate Section `[EXECUTIVE_SUMMARY]` placed before `[00_SECTION_AI_Readme]` if you want it visible to humans without scrolling through the full agent instruction block.

## Why keep both

- **Executive Summary** — humans scanning the canvas in 10 seconds understand what this template is, where to get the parser, and what they get.
- **Full System Instructions** (in `figjam-template-spec.md`) — the AI agent's operating manual. Loaded when an agent parses the board; too long for human scanning, but deterministic for the parser.

Both live in the repo so updates sync. FigJam canvas gets a copy of each as TEXT nodes.