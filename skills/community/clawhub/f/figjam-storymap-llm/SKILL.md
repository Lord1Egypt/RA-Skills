---
name: figjam-storymap-llm
description: Use when you need to parse or audit a FigJam User Story Map (Jeff Patton methodology) into LLM-readable Markdown or JSON — after a Story Mapping workshop, before publishing a Story Map template, or when feeding a Story Map to a coding agent (Cursor, Claude Code, Copilot).
---

# figjam-storymap-llm

Turn a FigJam Story Map into LLM-readable Markdown / JSON without manual transcription, OCR hallucinations, or loss of spatial semantics. Audits and parses FigJam boards built with Jeff Patton's User Story Mapping methodology.

## Purpose

Eliminate the manual transcription step after a Story Mapping workshop. Read the FigJam board via Figma REST API (deterministic, no OCR) and render a structured backlog that preserves Activity → Task → User Story hierarchy, release slicing (V1/V2/V3), acceptance criteria, owners, and connector relationships.

Built and validated on the real Story Map of a paid design-system product.

## When To Use

- After a Story Mapping workshop in FigJam — you want the board content as clean Markdown / JSON (no manual transcription), which you can then convert into a Notion page, Linear/Jira CSV import, or paste into a coding agent
- When you want to feed a Story Map to a coding agent (Cursor, Claude Code, Copilot) as living specification
- When auditing an existing FigJam Story Map for LLM-readiness before publishing the template
- When writing a case study or article based on a FigJam workshop and you need the workshop output as structured data

## When NOT To Use

- The FigJam board is empty or does not use Story Mapping methodology
- You want to programmatically edit FigJam (use Figma Plugin API instead)
- The file is a Figma design file (not a FigJam board) — use standard Figma MCP skills

## Inputs

- `file_key` from the FigJam URL (`figma.com/board/{file_key}/...`)
- A valid `FIGMA_TOKEN` (env var or CLI arg)
- Optional: a saved Figma JSON file path (instead of live API)

## Outputs

- **Audit mode:** Markdown report with PASS/FAIL per LLM-readiness criterion, plus concrete fix recommendations with node IDs
- **Parse mode (default):** `story-map.md` — structured backlog: Release → Activity → Task → User Story (with AC + Owner)
- **Parse mode (JSON):** `story-map.json` — structured data you can convert into a Notion DB, Linear/Jira CSV import, or feed to PM tooling via MCP

## Workflow

### Step 1 — Gather input (5 min)

- **Gold standard:** FigJam file key + valid FIGMA_TOKEN. Parser pulls JSON via REST API → 100% deterministic, no OCR.
- **Fallback (Vision):** Screenshot of the FigJam board. Less precise for >50 stickies.
- **Avoid:** PDF export — text becomes vectors, worst for (x, y) extraction.

### Step 2 — Audit LLM-readiness (10 min)

Run the Verification Prompt from `references/system-prompt.md` against the screenshot or JSON. The agent verifies:

1. **Backbone exists** — clear top-level `[ACT_*]` in Activities section and `[TASK_*]` in Tasks section
2. **Releases are separate sections** — `[03_SECTION_Release_1]`, `[04_SECTION_Release_2]`, `[05_SECTION_Release_3]`
3. **Taxonomy syntax** — every `[STORY]` sticky starts with `[STORY] [V*]`
4. **Lean UX rule** — V2 and V3 are clean (no `[P*]`, no `@Owner`) — Big Upfront Design is an anti-pattern
5. **AC inline** — acceptance criteria live in the same sticky as the story, not on a separate sticky
6. **Connectors meaningful** — only for branching and cross-release dependencies, not for linear flow
7. **Root wrapper** — all stickies inside the `[STORY_MAP]` root SECTION
8. **AI ReadMe** — `[00_SECTION_AI_Readme]` exists with legend, connector rules, expected output

Output: `audit-report.md` with PASS/FAIL per criterion and concrete node IDs to fix.

### Step 3 — Run the parser (10 min)

```bash
python scripts/figjam_parser.py --file-key {FILE_KEY} --token $FIGMA_TOKEN > story-map.md
python scripts/figjam_parser.py --file-key {FILE_KEY} --token $FIGMA_TOKEN --format json > story-map.json
```

The parser:

1. Fetches the object tree via Figma REST API (`/v1/files/{file_key}`)
2. Recursively traverses the document, identifying `SECTION`, `STICKY`, `SHAPE_WITH_TEXT`, `CONNECTOR`
3. Groups stickies by section
4. Maps each `[STORY]` to a `[TASK]` **algorithmically by X axis**:
   - Computes the center of the story (`x + width / 2`)
   - Assigns the story to the task whose X range contains that center
   - Fallback: nearest task center on X
5. Preserves connector relations (`connectorStart.endpointNodeId` → `connectorEnd.endpointNodeId`)
6. Renders Markdown grouped by Release → Activity → Task → User Story (with AC + Owner)

### Step 4 — Verify output (5 min)

Check `story-map.md`:

- Every `[STORY]` has a mapped `[TASK]` (or is flagged `UNASSIGNED`)
- AC is in the same section as the story
- V2 / V3 are clean (no `[P*]`, no `@Owner`)
- Connectors render as `A --[label]--> B`

### Step 5 — Use the parsed output (optional, conversion time varies)

The parser produces Markdown + JSON. From there you can:
- **Notion:** paste the Markdown as a page, or convert JSON to a `User Stories [DB]` with fields `Release`, `Priority`, `Owner`, `AC`, `Step` (relation) — conversion is manual or via Notion MCP
- **Linear / Jira:** convert `story-map.json` to the tool's CSV import format (converter not bundled) — or push via MCP
- **Cursor / Claude Code / Copilot:** paste Markdown as context for feature implementation — the agent sees the whole Story Map in one operation without scrolling Figma

## Taxonomy

### Canonical Story Map structure

```
[STORY_MAP]                                    ← root SECTION (wrapper)
├── [00_SECTION_AI_Readme]                     ← embedded system prompt + legend
├── [USER_SEGMENT_or_PERSONA]                  ← persona + Name + Description
├── [01_SECTION_BACKBONE_Activities]            ← [ACT_01] Activity, [ACT_02] Activity
├── [02_SECTION_BACKBONE_User_Tasks]           ← [TASK_01] Task, [TASK_02] Task, ...
├── [03_SECTION_Release_1] Core Value Proof    ← V1 (full taxonomy)
├── [04_SECTION_Release_2] Business Goal ...   ← V2 (clean)
└── [05_SECTION_Release_3] Business Goal ...   ← V3 (clean)
```

### Sticky syntax

```
[STORY] [V1] [P1] User Story sentence @DEV
Acceptance Criteria:
- Acceptance criterion 1
- Acceptance criterion 2
```

| Tag | Where | Meaning |
|---|---|---|
| `[STORY]` | Release section | User Story (release slice) |
| `[V1]` / `[V2]` / `[V3]` | In story sticky | Release identifier |
| `[P1]` / `[P2]` / `[P3]` | **V1 only** | Priority (Lean UX: skip in V2/V3) |
| `@UX` / `@DEV` / `@PM` / `@QA` | **V1 only** | Owner role (Lean UX: skip in V2/V3) |
| `[ACT_*]` | Backbone L1 | User Activity |
| `[TASK_*]` | Backbone L2 | User Task (Patton term — not "Step") |
| `Acceptance Criteria:` | Inside story sticky | Acceptance criteria inline |

### Why X-axis mapping

FigJam sections cannot form a 2D grid (Section × Section). So:

- **Sections for releases** (rows on Y axis)
- **Chronology encoded in X position** of `[TASK_*]` backbone cards
- **Stories mapped to tasks algorithmically** by `center_x` — you can drag stories around freely in the workshop without editing IDs; the parser tracks the column automatically

## Quality Checklist

- [ ] Every `[STORY]` has a `[V1]` / `[V2]` / `[V3]` prefix
- [ ] V2 and V3 are clean (no `[P*]`, no `@Owner`)
- [ ] Backbone: `[ACT_*]` in `[01_SECTION_BACKBONE_Activities]`, `[TASK_*]` in `[02_SECTION_BACKBONE_User_Tasks]`
- [ ] All stickies inside the `[STORY_MAP]` root SECTION (no `unsectioned_nodes`)
- [ ] AC lives in the same sticky as `[STORY]`, below the story sentence
- [ ] Connectors only for dependencies and branching (not linear flow)
- [ ] `[00_SECTION_AI_Readme]` exists and contains the legend + connector rules + expected output
- [ ] Internal text headers in each section (defense against `Copy as PNG` clipping section labels)

## Map Structure Guardian

When auditing a board or coaching a team during a Story Mapping workshop, the agent acts as a **Structure Guardian** — actively enforcing Patton + Cohn rules instead of passively reading the map. Run these checks before declaring the map ready for parsing.

### Backbone integrity (Patton)

- **Backbone is a user journey, not a feature list.** Activities and Tasks describe what the **user** does ("Buy Component Package", "Check External Documentation"), not what the team builds ("Build X", "Create Y"). Flag any `[ACT_*]` / `[TASK_*]` written in build-first voice as anti-pattern.
- **Every `[TASK_*]` carries at least one `[STORY]` in some release.** Empty tasks are either stale experiments or missing discovery work. Flag and ask the team to resolve.
- **Backbone is ordered chronologically left → right.** If tasks are shuffled or grouped by team instead of by user journey, flag for reordering before parsing.
- **Activity is optional grouping.** Use only when Tasks need context. Don't force Activities if the map is small — flat backbone of Tasks is valid Patton.

### Story quality (Cohn INVEST)

Each `[STORY]` in V1 should pass a quick INVEST sniff test:

- **Independent** — can be shipped without blocking another V1 story (or has explicit `[REQUIRES]` connector)
- **Negotiable** — has a sentence, not a fixed spec; AC are criteria, not implementation
- **Valuable** — the sentence states user value, not a technical task ("User logs in with Google" not "Implement OAuth")
- **Estimable** — has enough detail for story points (if `SP:` missing in V1, flag)
- **Small** — fits in one sprint; if the story is too big, suggest splitting before parsing
- **Testable** — has at least one AC; flag stories with empty AC section

### Scope creep detection

- **V1 horizontal slice is a walking skeleton, not a feature dump.** If V1 has more than ~12–15 stories per Activity, flag suspected scope creep and suggest cutting to MDP (Minimum Desirable Product — see `references/llm-ready-figjam-guidelines.md` §13).
- **No `[P*]` or `@Owner` in V2 / V3.** If found, this is Big Upfront Design — Lean UX anti-pattern. Flag and recommend removing.
- **Connectors crossing releases** (`[STORY_X_V2] --[REQUIRES]--> [STORY_Y_V1]`) are valid and expected; connectors inside the same release that create cycles suggest missed dependencies or duplicate stories.

### Coach behavior

When the guardian flags an issue, it does not silently fix — it reports the issue with node IDs / sticky names and proposes the smallest concrete fix:

> ⚠ `[STORY] [V1] [P1] Build login API @DEV` — build-first voice (Patton anti-pattern). Suggested rewrite: `[STORY] [V1] [P1] User signs in with Google @DEV`.


## Anti-patterns

- **Manual IDs on every story (`[TASK_01_01]`).** Editing dozens of cards when reorganizing = waste. Parser maps by X — don't write IDs on stories.
- **AC on a separate sticky.** Readable for humans, two disconnected objects in JSON for the agent. AC inline.
- **Priorities in V2 / V3.** Planning distant hypotheses = Big Upfront Design. Patton + Lean UX say: lying in the right section is enough.
- **`@Owner` in V2 / V3.** Assigning owners to functions that may never ship = noise. V1 only.
- **Connectors for linear flow.** Spaghetti payload in JSON. Chronology is encoded in X position + `[TASK_*]` numbering.
- **FigJam Stamps / Badges as information carriers.** Separate objects in JSON, not attached to the sticky. Use text prefixes in the sticky content.
- **Pen-tool lines as relations.** Vectors without `startNodeId` / `endNodeId`. Use native Connectors.
- **Missing `[STORY_MAP]` root.** Stickies on the bare canvas land in `unsectioned_nodes` and the parser ignores them.
- **Section names in natural language instead of tags.** `[SECTION: RELEASE 1]` vs `[03_SECTION_Release_1]` — the second gives deterministic prefixes for parsing. (Localized names like `[SECCIÓN: VERSIÓN 1]` or `[SEKCJA: WERSJA 1]` are the most common anti-pattern — they break prefix matching and force the agent to guess by Y position.)

## References

- `references/llm-ready-figjam-guidelines.md` — condensed guidelines for building LLM-ready FigJam boards, with industry source links
- `references/system-prompt.md` — System Prompt for an AI agent (audit mode + synthesis)
- `references/figjam-template-spec.md` — canonical FigJam template spec (colors, typography, sticky syntax, connectors, pre-publish checklist)
- `references/figjam-executive-summary.md` — human-facing canvas cover page (Executive Summary + ClawHub/GitHub links + Recommended Reading)
- `scripts/figjam_parser.py` — Python parser (Figma REST API → Markdown / JSON)
- **Published FigJam template (Figma Community):** [LLM Story Map — AI-readable User Story Map template](https://www.figma.com/community/file/1661156551667594442) — ready-to-use canvas built to this spec. Duplicate, replace `[PRODUCT NAME]`, fill the backbone, run the parser.

## Framework Credits

- **Jeff Patton — User Story Mapping** (O'Reilly, 2014). Backbone + Slices + Walking Skeleton. User Story Mapping is a methodology created by Jeff Patton. This skill applies its principles to digital canvas architectures.
- **Gothelf & Seiden — Lean UX** (2013). Hypothesis-driven, no Big Upfront Design in V2 / V3. MDP > MVP.
- **Teresa Torres — Continuous Discovery Habits** (2023). Story Map as living artifact in weekly discovery cadence; Opportunity-Solution Tree.
- **Eric Ries — The Lean Startup** (2011). Build-Measure-Learn loop; story map must be editable without waste.
- **Mike Cohn — User Stories Applied** (2004). INVEST, AC inline.
- **Figma REST API Documentation** — node types (SECTION, STICKY, CONNECTOR, SHAPE_WITH_TEXT).
- **Anthropic Vision Guidelines** — image and spatial data in Vision LLM prompts.
- **tldraw / Make Real** — open-source canvas-to-JSON architecture reference.

Full source list in `references/llm-ready-figjam-guidelines.md`.