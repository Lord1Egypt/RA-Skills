---
created: 2026-07-20
updated: 2026-07-20
version: 1.2
description: Canonical specification for the LLM-ready FigJam Story Map template (Patton methodology). Built and validated on a real design-system Story Map board.
---

# FigJam Story Map Template — LLM-ready (Patton methodology)

FigJam canvas template compliant with Jeff Patton's User Story Mapping methodology, optimised for error-free reading by LLMs (REST API JSON + Vision). Built and tested on a real design-system Story Map board.

## Canvas structure

```
[STORY_MAP]                                    ← root SECTION (wrapper, required)
├── [00_SECTION_AI_Readme]                     ← system prompt + legend
├── [TEMPLATE_META]                             ← attribution block (author, version, license, repo)
├── [USER_SEGMENT_or_PERSONA]                  ← persona + Name + Description (optional image)
├── [01_SECTION_BACKBONE_Activities]            ← backbone L1
│   └── [ACT_01] Activity  ·  [ACT_02] Activity
├── [02_SECTION_BACKBONE_User_Tasks]           ← backbone L2
│   └── [TASK_01] Task  ·  [TASK_02] Task  ·  [TASK_03] Task
├── [03_SECTION_Release_1] Core Value Proof     ← V1 with full taxonomy
├── [04_SECTION_Release_2] Business Goal ...    ← V2 clean
└── [05_SECTION_Release_3] Business Goal ...    ← V3 clean
```

## Template Metadata — attribution block `[TEMPLATE_META]`

Insert as a separate Section between `[00_SECTION_AI_Readme]` and `[USER_SEGMENT_or_PERSONA]`. The parser ignores it (it reads only STICKY / SHAPE_WITH_TEXT / CONNECTOR with `[STORY]` / `[ACT]` / `[TASK]` tags — this block is plain text). Clean separation of concerns: agent instructions in `[00]`, human attribution in `[TEMPLATE_META]`, map content in the remaining sections.

### Canonical `[TEMPLATE_META]` content

```text
Author: Monika Zapisek
Website: monikazapisek.com
Created: 2026-07-20
Last Updated: 2026-07-20
Version: 1.0
Licence: MIT
Skill: github.com/monikazapisek/design-engineering-playbook/tree/main/skills/figjam-storymap-llm
Get the skill (free, MIT): https://clawhub.ai/monikazapisekstudio/skills/figjam-storymap-llm

If you use this template, credit appreciated:
"Based on figjam-storymap-llm by Monika Zapisek"

FigJam and Figma are trademarks of Figma, Inc. This template is
independent and not affiliated with, endorsed by, or sponsored by Figma, Inc.
```

### What `[TEMPLATE_META]` must contain

| Field | Value | Why |
|---|---|---|
| Author | Full name | Build-in-public credit, social proof — anyone who duplicates the template sees the author |
| Website | Author URL | Profile visits → followers |
| Created | ISO 8601 date (`YYYY-MM-DD`) | When the template was created — tracking which version is in use |
| Last Updated | ISO 8601 date (`YYYY-MM-DD`) | Bump on every change — users know whether they have the fresh version |
| Version | semver (`1.0`, `1.1`, `2.0`) | Template versioning — important when the template is forked / duplicated |
| Licence | `MIT` (or other) | Explicit licence statement — users know whether they can duplicate / modify / sell |
| Skill (GitHub) | full URL to the skill folder in the repo | Opens the folder landing page (rendered README) — routes to parser, full procedure, source code |
| Skill (ClawHub) | `https://clawhub.ai/monikazapisekstudio/skills/figjam-storymap-llm` | ClawHub is a skills marketplace — one-click install for Claude Code / Cursor / Copilot. Prefer this link in templates (install path), GitHub as source-of-truth in skill repos |
| Credit appreciated | soft request for citation | Ethical ask (MIT does not require it), builds the authority loop — every screenshot of the template = free advertising |
| Trademark disclaimer | FigJam/Figma = Figma, Inc. | Defense-in-depth — nominative fair use is legal, disclaimer is a safety net |

### What NOT to put in `[TEMPLATE_META]`

- ❌ Full MIT licence text (21 lines — a repo link is enough)
- ❌ Contact email (spam risk — you have a Website)
- ❌ `© 2026 Monika Zapisek` — MIT LICENSE already contains it, do not duplicate
- ❌ "All rights reserved" — MIT is permissive, "all rights reserved" contradicts the licence
- ❌ Long skill description — that lives in the repo README, not on the canvas
- ❌ Follow / X handle — optional, only if you have an active account and want to build an audience

## Colour palette (semantic + deterministic for Vision LLM)

| Section / element | HEX | Meaning |
|---|---|---|
| `[ACT_*]` Activity | `#FFD9E2` / `rgba(255, 217, 226, 0.77)` | Backbone L1 — main user goal |
| `[TASK_*]` Task | `#FFE5D2` | Backbone L2 — step in the procedure |
| `[STORY] [V1]` | `#E6F6C3` (light green) | Release 1 — MVP / Core Value |
| `[STORY] [V2]` | `#E5F3FE` (light blue) | Release 2 — Growth |
| `[STORY] [V3]` | `#F3EEFF` (light purple) | Release 3 — Scale / Vision |
| Persona (sticky) | `#B3EFBD`, `#B3F4EF`, `#FFD3A8`, `#D3BDFF` | 4 segments: Designer / Developer / End-user / AI-agent |
| Connectors (default) | `#D5C2C5` | Causal relations |
| Connectors (block) | red | Blockers (A BLOCKS B) |

## Typography

- **Title (Story Map):** Inter Bold 96px
- **Section header (Activity / Task / Release):** Inter Bold 96px, section colour
- **Description text:** Inter Medium 40px, section colour
- **Sticky text:** Inter Medium 16px

## Sticky tag taxonomy

### Story (V1 — full)

```text
[STORY] [V1] [P1] User Story sentence @DEV
Acceptance Criteria:
- Acceptance criterion 1
- Acceptance criterion 2
```

### Story (V2 / V3 — clean)

```text
[STORY] [V2] User Story sentence
Acceptance Criteria:
- Acceptance criterion 1
```

**Zero `[P*]`, zero `@Owner` in V2/V3** (Lean UX — planning distant hypotheses is Big Upfront Design).

### Activity (backbone L1)

```text
[ACT_01] Activity
```

### Task (backbone L2)

```text
[TASK_01] Task
```

## Layout (X and Y axes)

- **X axis (chronology):** left → right. `[ACT_01]` → `[ACT_02]`, within an activity `[TASK_01]` → `[TASK_02]` → `[TASK_03]`. Each task is its own column.
- **Y axis (priority / release):** top → bottom. Backbone at the top (Activities, then Tasks), release slices below (V1, V2, V3).
- **Story in a release:** a `[STORY]` sticky stacks vertically under the task it belongs to (parser algorithm: `center_x` of the story must fall within the task's X range).
- **Column spacing:** 40–60 px horizontally — gives the algorithm a large error margin.
- **Do not overlap columns:** as long as a sticky from one column does not slide more than halfway under the neighbouring task, the parser will not misfire.

## Connectors

### When to use

- **Branching (alternative flows):** `[STORY_05] --[IF_FAIL]--> [STORY_05B] Error screen`
- **Cross-release dependencies:** `[STORY_12_V2] --[REQUIRES]--> [STORY_03_V1]`
- **Acceptance criteria / notes:** a clarifying sticky attached to the main story (though AC inline in the same sticky is preferred)

### When NOT to use

- **Linear chronological flow** (step 1 → step 2 → step 3). Chronology is encoded in X position + `[TASK_*]` numbering. 100 arrows = spaghetti payload.

## `[00_SECTION_AI_Readme]` — agent instruction

Insert at the start of the canvas (ideally `x: 0, y: 0` relative to the root). This is the agent's brain on the canvas — without it the agent guesses, with it the agent acts deterministically. Insert as **a single TEXT node** (do not split into separate stickies — the agent reads this as one instruction document).

```text
==================================================
SYSTEM INSTRUCTIONS FOR AI AGENT (FIGJAM PARSER)
==================================================

You are parsing a FigJam Story Map built with Jeff Patton's User Story Mapping
methodology. This is a living specification, not a screenshot. Treat every sticky
as a structured record, every section as a container, every connector as a
semantic relation. Do not guess. Do not invent. Flag what is ambiguous.

--------------------------------------------------
PURPOSE
--------------------------------------------------
This file contains a Story Map for the product [PRODUCT NAME].
Parse it into a structured backlog (Release -> Activity -> Task -> User Story
with Acceptance Criteria + Owner) without manual transcription.

--------------------------------------------------
SKILL (provenance + install)
--------------------------------------------------
This FigJam template is part of the figjam-storymap-llm skill by Monika Zapisek.
The skill audits and parses FigJam User Story Maps into LLM-readable
Markdown / JSON - eliminates the post-workshop transcription step and feeds
Story Maps to coding agents (Cursor, Claude Code, Copilot) as living spec.

What you get:
- Python parser (Figma REST API -> Markdown / JSON)
- Canonical FigJam template spec (this file's structure)
- Verification prompt for LLM-readiness audits
- Map Structure Guardian (active coach for Patton + Cohn INVEST rules)
- Lean UX rules baked in (V1 tagged, V2 / V3 clean)

Get the skill (free, MIT licence):
https://clawhub.ai/monikazapisekstudio/skills/figjam-storymap-llm

Install:
- Claude Code / Cursor / Copilot: load the SKILL.md from the link above
- CLI parser: clone the repo, run
  scripts/figjam_parser.py --file-key {KEY} --token $FIGMA_TOKEN
- Audit mode: paste references/system-prompt.md as System Instructions,
  share board screenshot

--------------------------------------------------
CANVAS STRUCTURE
--------------------------------------------------
- Root: [STORY_MAP] - ALL stickies must be inside it.
  Anything outside lands in unsectioned_nodes and the parser ignores it.
- Sections stacked vertically (Y axis), top to bottom:
  [00_SECTION_AI_Readme]             <- this instruction block
  [TEMPLATE_META]                     <- attribution (author, version, licence)
  [USER_SEGMENT_or_PERSONA]           <- who the map is for
  [01_SECTION_BACKBONE_Activities]    <- backbone L1: [ACT_*]
  [02_SECTION_BACKBONE_User_Tasks]    <- backbone L2: [TASK_*]
  [03_SECTION_Release_1] Core Value Proof   <- V1 (full taxonomy)
  [04_SECTION_Release_2] Business Goal ...  <- V2 (clean)
  [05_SECTION_Release_3] Business Goal ...  <- V3 (clean)
- Chronology is encoded in the X axis (left -> right).
  [ACT_01] -> [ACT_02] -> ...
  [TASK_01] -> [TASK_02] -> [TASK_03] (within an activity, left -> right)
- Every [STORY] is mapped to a [TASK] algorithmically by X position:
  story_center_x = story.x + story.width / 2
  find the [TASK] whose range (task.x .. task.x + task.width) contains story_center_x
  fallback: nearest task center on X (within 400 px); otherwise UNASSIGNED.
  This means the team can drag stories around freely - the parser tracks the column.

--------------------------------------------------
COLOR SEMANTICS
--------------------------------------------------
#FFD9E2 = Activity  (backbone L1, main user goal)
#FFE5D2 = Task      (backbone L2, discrete user action - Patton term, NOT "Step")
#E6F6C3 = Story V1  (MVP / Core Value Proof - full taxonomy: [P*] + @Owner + AC)
#E5F3FE = Story V2  (Growth - clean)
#F3EEFF = Story V3  (Scale / Vision - clean)
#D5C2C5 = Connector (causal relation)
red     = Connector blocker (A BLOCKS B)

Colour is just a HEX in JSON. The agent does not know that yellow = risk unless
this legend says so. Text prefixes on the sticky are the deterministic carrier.

--------------------------------------------------
TAXONOMY (canonical sticky syntax)
--------------------------------------------------
V1 story (full):
  [STORY] [V1] [P1] User Story sentence @DEV
  Acceptance Criteria:
  - Acceptance criterion 1
  - Acceptance criterion 2

V2 / V3 story (clean - no [P*], no @Owner):
  [STORY] [V2] User Story sentence
  Acceptance Criteria:
  - Acceptance criterion 1

Activity (backbone L1):  [ACT_01] Activity name
Task    (backbone L2):  [TASK_01] Task name

--------------------------------------------------
TAGS
--------------------------------------------------
[STORY]                = User Story (release slice)
[V1] / [V2] / [V3]     = Release identifier
[P1] / [P2] / [P3]     = Priority - V1 ONLY
@UX / @DEV / @PM / @QA = Owner role - V1 ONLY
[ACT_*]                = User Activity (backbone L1, major user goal)
[TASK_*]               = User Task    (backbone L2, step in journey - Patton term, NOT "Step")
Acceptance Criteria:   = AC section inside the story sticky (NOT a separate sticky)

--------------------------------------------------
LEAN UX RULES (HARD)
--------------------------------------------------
- V1 (MVP): full taxonomy - [P1]/[P2]/[P3] + @Owner + Acceptance Criteria inline
- V2 / V3: clean - zero [P*], zero @Owner, zero priority assignment
- Reason: planning executors / priorities for distant hypotheses is Big Upfront Design
  (Patton + Gothelf & Seiden, Lean UX). V2 / V3 will change after V1 hits the market.
- Exception: none. If you find [P*] or @Owner in V2/V3, FLAG as anti-pattern with
  the sticky node ID and propose removing the tag.

--------------------------------------------------
CONNECTOR RULES
--------------------------------------------------
- Arrow A -> B            = causal relation (A causes / enables / requires B)
- Red edge                = blocker (A BLOCKS B)
- Edge label              = relation type (REQUIRES, IF_FAIL, BLOCKS)
- Cross-release connectors are valid and expected:
  [STORY_X_V2] --[REQUIRES]--> [STORY_Y_V1]
- DO NOT connect linearly (step 1 -> step 2 -> step 3). Chronology is encoded
  in X position + [TASK_*] numbering. 100 arrows = spaghetti payload in JSON.
- Use native FigJam Connectors only (they carry connectorStart / connectorEnd
  in JSON). Pen-tool lines are vectors without relation semantics - ignore them.
- FigJam Stamps / Badges are separate objects in JSON, not attached to the
  sticky. Use text prefixes inside the sticky content, never stamps as
  information carriers.

--------------------------------------------------
ACCEPTANCE CRITERIA RULES (HARD)
--------------------------------------------------
- AC lives in the SAME sticky as [STORY], below the story sentence,
  after the "Acceptance Criteria:" marker on its own line.
- A separate AC sticky next to the Story = anti-pattern. It becomes two
  disconnected JSON objects and the agent must guess the relation by (x, y).
- If you see a separate AC sticky, FLAG it and propose merging with the
  nearest Story. Do not silently merge - report so the team learns the pattern.

--------------------------------------------------
PARSING METHODS (best to worst)
--------------------------------------------------

1. GOLD STANDARD - Figma REST API (JSON)
   URL:      https://www.figma.com/developers/api
   Endpoint: GET /v1/files/{file_key}
   Auth:     header X-Figma-Token
   How:      fetches full node tree (SECTION, STICKY, SHAPE_WITH_TEXT, CONNECTOR)
   Pros:     100% deterministic, zero OCR, zero hallucinations,
             full metadata (x, y, section, connectorStart/End)
   Cons:     requires a valid FIGMA_TOKEN (Figma personal access token)
   Use when: production, large boards (>50 stickies), repeated parsing

2. FALLBACK - PNG / screenshot (Vision LLM)
   How:      FigJam screenshot -> Claude / GPT-4o (Vision mode)
   Pros:     quick, no API token needed
   Cons:
   - OCR errors on >100 stickies (small text)
   - Section names may be clipped by Copy as PNG (label renders on outer frame edge)
   - No spatial metadata (x, y) - agent loses story -> task mapping
   - Dense layouts confuse the agent
   Defense:  add internal text headers inside each section
             (do not rely only on the frame label)
   Use when: quick audit, small boards (<50 stickies), no API token

3. NOT RECOMMENDED - PDF export
   Why NOT:
   - PDF export converts text to vectors / text streams
   - Spatial dependency extraction (x, y) is most error-prone
   - Section hierarchy is often lost (PDF does not preserve FigJam hierarchy)
   - Connectors become lines without relation semantics
   Do not use. If you only have PDF, route through Figma REST API (JSON) instead.

--------------------------------------------------
PARSING PROCEDURE (execute in this order)
--------------------------------------------------
1. Locate [STORY_MAP] root SECTION. Anything outside it -> flag UNSECTIONED.
2. Read [00_SECTION_AI_Readme] (this block) - it is the agent's operating manual.
3. Read [USER_SEGMENT_or_PERSONA] - the map is meaningless without knowing
   who the user is. Carry persona context into every story interpretation.
4. Walk [01_SECTION_BACKBONE_Activities] -> list of [ACT_*].
5. Walk [02_SECTION_BACKBONE_User_Tasks] -> list of [TASK_*] with x, width.
6. For each release section [03_..] [04_..] [05_..]:
   - Identify every [STORY] sticky inside the section.
   - Parse tags: [V*] -> release, [P*] -> priority (V1 only), @role -> owner (V1 only).
   - Split the sticky text at "Acceptance Criteria:" on its own line.
     Body above  -> story sentence (strip tags and @roles).
     Body below  -> acceptance criteria lines (one per bullet or newline).
   - Map story -> task by X: story_center_x falls into a task's X range.
     Fallback: nearest task center within 400 px, else UNASSIGNED.
   - Map task  -> activity by X overlap (activity sits above its tasks in the same column).
7. Collect native Connectors. Ignore pen-tool lines. Ignore Stamps / Badges.
8. Render Markdown grouped by Release -> Activity -> Task -> User Stories
   (with Acceptance Criteria + Owner).
9. Run the FLAG audit (see below) and append the report.

--------------------------------------------------
OUTPUT EXPECTED
--------------------------------------------------
Markdown backlog ordered:
  Release -> Activity -> Task -> User Stories (with Acceptance Criteria + Owner)

For each [STORY]:
  - [STORY] [V1] [P1] <story sentence> @DEV
    - **Acceptance Criteria:**
      - <criterion 1>
      - <criterion 2>
  - mapped to: <TASK name>
  - section:   <section name>

For each Connector:
  - <from_id> --[label]--> <to_id>

For each warning:
  - <node_id>: <issue> -> <smallest concrete fix>

--------------------------------------------------
FLAG (active coach - do NOT silently fix)
--------------------------------------------------
The agent is a Structure Guardian, not a passive reader. When you detect an
anti-pattern, report it with the sticky node ID and the smallest concrete fix.
Do not rewrite the sticky in place - report so the team learns the pattern.

Flag when you see:
- Build-first voice in [ACT_*] / [TASK_*] ("Build X" instead of "User does X")
  -> Patton anti-pattern. Suggest rewrite in user voice.
- V2 / V3 with [P*] or @Owner
  -> Big Upfront Design. Suggest removing the tag.
- Separate Acceptance Criteria sticky next to a Story
  -> two disconnected JSON objects. Suggest merging AC into the story sticky
     after the "Acceptance Criteria:" marker.
- Stickies outside [STORY_MAP] root
  -> unsectioned_nodes, parser will not find them. Suggest moving inside root.
- Connector cycles within the same release
  -> suspected duplicate Story or missing dependency. Suggest resolving.
- Connectors for linear flow (step 1 -> step 2 -> step 3)
  -> spaghetti payload. Chronology is in X + [TASK_*] numbering. Suggest removing.
- [STORY] missing [V*] tag
  -> release cannot be inferred from position alone. Suggest adding [V1]/[V2]/[V3].
- [STORY] with no Acceptance Criteria section
  -> not testable (Cohn INVEST "T"). Suggest writing at least one AC line.
- [STORY] in build-first voice ("Implement OAuth" instead of "User signs in with Google")
  -> story map is user perspective, not builder perspective. Suggest rewrite.
- Empty [TASK_*] (no story in any release)
  -> dead experiment or missing discovery. Suggest resolving (cut or populate).

--------------------------------------------------
WHAT NOT TO DO
--------------------------------------------------
- Do not silently fix anti-patterns. Report + propose the smallest concrete change.
- Do not infer [V*] from Y position alone. The tag on the sticky is the source of truth.
- Do not assign [P*] or @Owner to V2 / V3 stories "to help the team".
  Lean UX is explicit: hypotheses stay clean.
- Do not treat FigJam Stamps / Badges as information carriers.
  They are separate JSON objects, not attached to the sticky.
- Do not treat pen-tool lines as connectors.
  They are vectors without connectorStart / connectorEnd.
- Do not trust PDF export. Route through Figma REST API instead.
- Do not split Acceptance Criteria into a separate sticky.
- Do not number stories with manual IDs like [STORY_01_03].
  Mapping is algorithmic by X. Manual IDs are waste.

--------------------------------------------------
RECOMMENDED READING
--------------------------------------------------
This Story Map template & skill integrates the following world-class agile
methodologies:

- User Story Mapping (Jeff Patton): The core 2D structure (Horizontal Sequence
  / Vertical Slices) is based on Patton's technique for building shared
  understanding and visualizing the 'Walking Skeleton'.

- Better User Stories (Mike Cohn): The hierarchy of Activities, Tasks, and
  Stories, along with the 'Significant Objective' framing, follows Cohn's
  strategic approach to backlog refinement.

- Continuous Discovery Habits (Teresa Torres): The 'Problem Framing' and
  'Strategic Context' placeholders ensure that the map remains aligned with
  validated user opportunities and business outcomes.

- Escaping the Build Trap (Melissa Perri): The release strategy (V1-V3) is
  designed to prioritize validated value over simple output, ensuring the
  team solves real business problems.

- Lean UX (Jeff Gothelf & Josh Seiden): The inclusion of 'Core Value Proof'
  in V1 reflects the hypothesis-driven approach to product design.
==================================================
```

**Tip:** In the block above, replace `[PRODUCT NAME]` with the actual product name before publishing the template.

## Pre-publish checklist (10 min)

Before publishing the template as an "LLM-ready FigJam Story Map", verify:

- [ ] **Root `[STORY_MAP]`** wraps the entire canvas (zero `unsectioned_nodes` in JSON)
- [ ] **`[00_SECTION_AI_Readme]`** exists and contains legend + connector rules + expected output
- [ ] **`[TEMPLATE_META]`** exists between `[00]` and `[USER_SEGMENT]` — contains Author, Created, Last Updated, Version, Licence, Skill URL, credit appreciated, trademark disclaimer
- [ ] **`[01_SECTION_BACKBONE_Activities]`** contains only `[ACT_*]`
- [ ] **`[02_SECTION_BACKBONE_User_Tasks]`** contains only `[TASK_*]`, columns have 40–60 px spacing
- [ ] **`[03_SECTION_Release_1] Core Value Proof`** — `[STORY] [V1]` stickies with `[P1]/[P2]/[P3]`, `@Owner`, AC inline
- [ ] **`[04_SECTION_Release_2]`** and **`[05_SECTION_Release_3]`** — `[STORY] [V2]/[V3]` stickies clean (zero `[P*]`, zero `@Owner`)
- [ ] **AC inline** — in the same sticky as `[STORY]`, after `Acceptance Criteria:`
- [ ] **Connectors** only for branching / cross-release dependencies
- [ ] **Internal text headers** in each section (defense against `Copy as PNG` clipping section labels)
- [ ] **No FigJam Stamps / Badges** as information carriers (use text prefixes inside the sticky instead)
- [ ] **`Last Updated`** in `[TEMPLATE_META]` refreshed before publishing (today's ISO 8601 date)

## Parser test (after filling the template)

```bash
python scripts/figjam_parser.py --file-key {FILE_KEY} --token $FIGMA_TOKEN > story-map.md
```

Verify:

- Each `[STORY]` has an assigned `[TASK]` (or is flagged `UNASSIGNED`)
- AC stays in the same section as the story
- V2 / V3 are clean
- Connectors render as `A --[label]--> B`

## Pattoian notes (Patton + Lean UX)

- **Release naming:** `Core Value Proof`, `Business Goal or Outcome` — outcome, not "v2 for v2". Patton encourages giving a short business goal next to the version number.
- **Priorities only in V1:** position on the Y axis within V1 + `[P1]/[P2]/[P3]` inside the release. V2 / V3 are hypotheses.
- **Owner only in V1:** assigning owners to distant features is noise.
- **Story Map = user perspective, not builder perspective.** Activities / Steps describe what the **user** does ("Buy Component Package", "Check External Documentation"), not what the team builds ("Build X", "Create Y").
- **Term "Task" (not "Step").** Patton standard for backbone L2.