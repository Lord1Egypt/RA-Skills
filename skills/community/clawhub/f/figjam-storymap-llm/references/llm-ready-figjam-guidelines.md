---
created: 2026-07-20
updated: 2026-07-20
version: 1.1
description: Condensed "AI-Ready FigJam" guidelines — how to build FigJam boards so they are read error-free by LLMs (Vision and REST API). With industry references.
---

# LLM-Ready FigJam — guidelines

Best practices collected from R&D teams working with Vision LLMs and Figma AI tools. Figma has not released an official "Design for AI Agents" document — these guidelines are an unofficial standard gathered by LLM researchers.

## 1. Spatial architecture (semantics over reading from thin air)

Agents handle tree hierarchies far better than free-form spatial layouts.

- **Sections (Section / Frame) as context containers.** An agent gets lost in open space. Wrap logical areas in sections and give them unambiguous names (`[03_SECTION_Release_1] Core Value Proof`).
- **Reading order Z-pattern / F-pattern.** Sections and matrices left to right, top to bottom. Agents process objects by X / Y coordinates or sequentially from the layer tree.
- **Explicit matrix titles.** Do not rely on a sticky's position in the top-right corner. Add axis or quadrant headers as separate text labels.
- **Root SECTION wrapper.** In FigJam, wrap everything in one root SECTION (`[STORY_MAP]`). Without it, stickies end up in `unsectioned_nodes` in JSON.

## 2. Internal text headers (defense against losing the section name)

In FigJam, the SECTION name renders on the outer edge of the frame. `Copy as PNG` clips the label or renders it outside the frame.

- **Insert a plain text block inside each section** with a header (`### SECTION: V1_MVP (Core Value)`). No matter what you select for export, the header always lands on the screenshot.
- **Click the SECTION name, not the stickies**, to select the whole frame with its label.
- **Export panel → PNG → Include background** preserves labels and backgrounds.
- **REST API parser** bypasses this issue — it reads `node.name` from JSON regardless of screenshot visibility.

## 3. Sticky notes — syntax and taxonomy

Mixing colours and free text = agent hallucinations. The most deterministic method (for both JSON and Vision) is **prefix taxonomy in square brackets**.

### Canonical syntax

```
[TYPE] [PRIORITY] Actual content [METADATA]
```

### Prefixes

| Category | Tags | Example |
|---|---|---|
| Element type | `[INSIGHT]`, `[PROBLEM]`, `[IDEA]`, `[RISK]`, `[DECISION]`, `[ACTION]`, `[STORY]`, `[ACT]`, `[TASK]` | `[PROBLEM] Cart does not remember the chosen delivery method.` |
| Priority | `[P1]`, `[P2]`, `[P3]` or `[MUST]`, `[SHOULD]`, `[COULD]` | `[IDEA] [P1] Fast BLIK checkout.` |
| State / status | `[OPEN]`, `[IN_REVIEW]`, `[DONE]`, `[BLOCKED]` | `[ACTION] [BLOCKED] Legal review of terms.` |
| Assignment | `@UX`, `@DEV`, `@PM`, `@QA` | `[ACTION] Check GA4 event logs. @DEV` |
| Release | `[V1]`, `[V2]`, `[V3]` | `[STORY] [V1] [P1] ... @DEV` |

### Why not native FigJam Badges / Stamps?

Stamps and stickers in FigJam are separate vector objects in JSON (`STAMP` / `STICKER`), often not connected to the sticky by a parent-child relation. For an agent reading the tree, they are separate icons lying nearby. A text prefix typed inside the sticky is unambiguous.

## 4. `[00_SECTION_AI_ReadMe]` — system prompt embedded in the canvas

A section at the start of the canvas (ideally `x: 0, y: 0` relative to the root) as operating instructions for the agent — especially useful for Vision LLMs and PNG export.

Example content:

```text
==================================================
SYSTEM INSTRUCTIONS FOR AI AGENT (FIGJAM PARSER)
==================================================
PURPOSE:
This file contains a UX workshop synthesis divided into sections.

CANVAS STRUCTURE:
- Sections laid out horizontally: [01_BACKBONE_Activities] -> [02_BACKBONE_User_Tasks] -> [03_Release_1] -> [04_Release_2] -> [05_Release_3]

COLOR SEMANTICS:
- Green (#B3EFBD) = Activities (backbone L1)
- Cyan (#B3F4EF) = Tasks (backbone L2)
- Orange (#FFD3A8) = Release 1 (V1, MVP)
- Purple (#D3BDFF) = Release 2 / 3 (V2/V3, hypotheses)

CONNECTOR RULES:
- Arrow A -> B = causal relation (A causes B)
- Red edges = blockers (A BLOCKS B)

OUTPUT EXPECTED:
Markdown backlog divided: Release -> Activity -> Task -> User Stories (with AC + Owner)
==================================================
```

## 5. Spatial semantics for matrices

A FigJam Section cannot form a classic 2D grid (Section × Section). Hybrid solution for LLMs:

- **Sections for rows (Releases):** main logical containers in JSON (`[03_SECTION_Release_1]`, `[04_SECTION_Release_2]`).
- **Chronology (X axis) encoded in task identifiers or X position:** `[TASK_01]`, `[TASK_02]`, `[TASK_03]` in the backbone. Each `[STORY]` in a release inherits the identifier of the task it sits under — **algorithmically by X axis**, not by manual IDs on stickies.
- **Explicit axis labels** for matrices (optional): `[AXIS_X_MIN]`, `[AXIS_X_MAX]`, `[AXIS_Y_MIN]`, `[AXIS_Y_MAX]`.

## 6. Relations and connectors

### When to USE

- **Branching (alternative flows):** `[STORY_05] --[IF_FAIL]--> [STORY_05B] Error screen`.
- **Hard cross-release dependencies:** `[STORY_12_V2] --[REQUIRES]--> [STORY_03_V1]`.
- **Acceptance criteria / notes:** a clarifying sticky attached to the main story (though AC inline in the same sticky is preferred).

### When to AVOID

- **Linear chronological flow** (step 1 → step 2 → step 3). 100 arrows = spaghetti payload in JSON. The agent reads chronology from X position + `[TASK_*]` numbering.

### Figma API — Connector fields

- `connectorStart.endpointNodeId` — start node ID
- `connectorEnd.endpointNodeId` — end node ID
- `characters` — relation text label

Use **native Connectors** (not pen-tool lines — those are a set of vectors in JSON without relation semantics).

## 7. Parsing — when to use what

| Method | When | Pros | Cons |
|---|---|---|---|
| **Figma REST API (JSON)** | Production, large boards, >50 stickies | 100% deterministic, zero OCR, low token cost, full metadata (x, y, section, connectors) | Requires a valid `FIGMA_TOKEN` |
| **Vision LLM (PNG)** | Quick paste, small boards | No API token needed | OCR errors on >100 stickies, loss of spatial metadata |
| **PDF export** | NEVER | — | Text vectors, worst for (x, y) extraction |

## 8. Colour semantics

Colour in JSON is just HEX. The agent does not know that yellow = risk unless it has a legend.

- **Legend section in `[00_SECTION_AI_ReadMe]`** (Red = Blocker, Green = Idea)
- **Text prefixes on stickies** (deterministic, read by both JSON and Vision)

## 9. Canvas hygiene (3 rules for X-axis mapping)

- **Stack vertically:** stickies from the same task one below the other.
- **Keep 40–60 px gaps between columns:** gives the algorithm a large error margin.
- **Do not overlap columns:** as long as a sticky from one column does not slide more than halfway under the neighbouring task, the parser will not misfire.

## 10. Lean UX — priorities and owners only in V1

- **V1 (MVP):** precise — `[P1]/[P2]/[P3]` + `@Owner` (UX/DEV/PM), because it enters the nearest sprint.
- **V2, V3:** options and hypotheses — zero priorities, zero owners. Planning executors for releases that will change after V1 hits the market is Big Upfront Design (Patton + Lean UX).

## 11. AC inline (in the same sticky as the Story)

- **Acceptance criteria in the same sticky as `[STORY]`**, below the story sentence, after `Acceptance Criteria:`.
- A separate sticky next to the Story = two disconnected objects in JSON — the agent must guess the relation by (x, y).

## 12. Patton dictionary (official terms)

| Concept | Tag | Level |
|---|---|---|
| User Activity | `[ACT_01]`, `[ACT_02]` | Backbone L1 (main user goal) |
| User Task | `[TASK_01]`, `[TASK_02]` | Backbone L2 (step in the procedure) |
| User Story | `[STORY]` | Release (slice of functionality) |
| Release Slice / Version | `[V1]`, `[V2]`, `[V3]` | Horizontal row |
| Backbone | `[01_SECTION_BACKBONE_Activities]` + `[02_SECTION_BACKBONE_User_Tasks]` | Static header structure |
| User Journey | Chronological flow along the X axis | Process concept (time) |

**Use `Task`, not `Step`.** "Step" is a User Journey Mapping term, but in Patton's Story Mapping the industry standard is `Task`.

## 13. Product Discovery — MDP, Torres, Gothelf

A Story Map is a discovery artifact, not an execution backlog. It lives in the triangle of Patton (structure) + Gothelf (Lean UX) + Torres (Continuous Discovery). These three principles protect the team from scope creep and from treating V2 / V3 as "everything else".

### MDP > MVP (Minimum Desirable Product)

- **MVP** (Minimum Viable Product) asks: "what is the least we can ship so it works?"
- **MDP** (Minimum Desirable Product) asks: "what is the least we can ship so the user **wants** it?"
- In Story Mapping, V1 should be MDP, not MVP. A slice that is only viable but not desirable teaches the wrong signal — the user does not use it, you get no feedback, you waste a sprint.
- In practice: if V1 has >12–15 stories per Activity, it is probably MVP, not MDP. Cut to the experience the user actually wants (not "everything needed for it to work at all").
- Source: Gothelf & Seiden, *Lean UX* (2013) — hypothesis-driven; Torres, *Continuous Discovery Habits* (2023) — opportunity-solution tree powered by weekly interviews.

### Torres — Continuous Discovery cadence

A Story Map is not a one-off workshop. It is a living artifact, updated in the rhythm of Continuous Discovery:

- **Weekly opportunity interviews** → you discover new opportunities
- **Opportunity-Solution Tree (OST)** → you map opportunities → solutions → experiments
- **Story Map updates** → a new `[ACT_*]` or `[TASK_*]` only when a new discovery area opens; in existing Tasks you add stories to the relevant release
- **V1 frozen during the sprint** — V2 / V3 open to hypotheses from interviews
- Source: Teresa Torres, *Continuous Discovery Habits* (2023) — https://www.producttalk.org/

### Gothelf — Lean UX in the Story Map

- **A Story Map is a hypothesis, not a specification.** Each `[STORY]` is "we believe user X wants Y to achieve Z" — not "we build Y".
- **V2 / V3 clean (zero `[P*]`, zero `@Owner`)** = the key Lean UX rule. Planning executors and priorities for hypotheses is Big Upfront Design. V1 will be verified by the market, V2 / V3 will change.
- **Outcome over output.** Release names with a business goal (`Core Value Proof`, `Business Goal or Outcome`), not "v2 for v2". Patton encourages giving a short business goal next to the version number.
- **Build-Measure-Learn loop** (Ries): V1 → ship → measure → learn → update V2 / V3 (or cancel). The Story Map must be editable without waste — that is why `figjam-storymap-llm` parses algorithmically by X axis, so the team can drag stickies around without rewriting IDs.
- Source: Gothelf & Seiden, *Lean UX* (2013); Eric Ries, *The Lean Startup* (2011).

### Scope creep — warning signs in the Story Map

- V1 > 12–15 stories per Activity → probably MVP, not MDP
- V2 / V3 with `[P*]` or `@Owner` → Big Upfront Design
- `[STORY]` in build-first voice ("Build X", "Implement Y") → Patton anti-pattern (story map = user perspective)
- Empty `[TASK_*]` (no story in any release) → either a dead experiment or missing discovery
- Connector cycles within the same release → suspected duplicate story or missing dependency
- Connectors for linear flow (step 1 → step 2 → step 3) → spaghetti payload, chronology encoded in X + `[TASK_*]` numbering

### Coaching stance

An agent working with a Story Map is not a passive reader — it is a **Structure Guardian**:

- Flag the issue with the node ID / sticky name
- Propose the smallest concrete change (not "refactor this", but "change `[STORY] [V1] Build login API @DEV` to `[STORY] [V1] User signs in with Google @DEV`")
- Do not silently fix — report, so the team learns the pattern
- Ask before cutting scope: "is this viable or desirable?" — forces MDP, not MVP

---

## Industry references

### Official documentation and data structures

- **Figma REST API Documentation — Node Types** — https://www.figma.com/developers/api
  Structure description: SECTION, STICKY, CONNECTOR, WIDGET, SHAPE_WITH_TEXT in the JSON tree. FigJam-specific: https://www.figma.com/developers/api#figjam-nodes

- **Figma Plugin API — StickyNode & SectionNode** — https://www.figma.com/plugin-docs/
  FigJam object properties accessible programmatically (colour, author, textContent, boundingBox).

### Spatial prompting standards and Vision LLM

- **Anthropic Claude Vision — Image & Layout Guidelines** — https://docs.anthropic.com/en/docs/build-with-claude/vision
  Guidelines for feeding images, diagrams and spatial structures to vision models.

- **OpenAI Cookbook — Processing Spatial & Visual Data** — https://cookbook.openai.com/
  Best practices for tabular structures, charts and screenshots to GPT-4o.

- **OpenAI GPT-4o Vision System Card** — https://openai.com/index/hello-gpt-4o/
  OCR limitations in dense layouts and structuring recommendations.

### Canvas-to-JSON architectures (open-source references)

- **tldraw / Make Real Documentation** — https://github.com/tldraw/tldraw / https://makereal.tldraw.com/
  One of the most advanced projects combining an infinite canvas with AI agents. Its architecture of transcribing shapes into prompts (Canvas-to-Code / Canvas-to-JSON) is the current industry standard for whiteboard tools.

- **Excalidraw + AI experiments** — https://github.com/excalidraw/excalidraw
  Open-source alternative, useful for comparing canvas → structure patterns.

### Methodology (canonical sources)

- **Jeff Patton — User Story Mapping** (O'Reilly, 2014) — https://www.oreilly.com/library/view/user-story-mapping/9781491973899/
  Backbone + Slices + Walking Skeleton.

- **Jeff Patton — www.jpattonassociates.com** — https://www.jpattonassociates.com/user-story-mapping/
  Author commentary, patterns, case studies.

- **Lean UX (Gothelf & Seiden, 2013)** — https://www.jeffgothelf.com/lean-ux-book/
  Hypothesis-driven, MVPs, collaborative design, fighting Big Upfront Design.

- **Mike Cohn — User Stories Applied (2004)** — https://www.mountaingoatsoftware.com/books/user-stories-applied
  INVEST, AC inline, story splitting.

- **Mountain Goat Software — Better User Stories course** — https://www.mountaingoatsoftware.com/courses/better-user-stories
  Course transcript used in `agent-agile-master`.

- **Teresa Torres — Continuous Discovery Habits (2023)** — https://www.producttalk.org/
  Story Map as a living artifact in a weekly discovery cadence; Opportunity-Solution Tree.

- **Eric Ries — The Lean Startup (2011)** — http://theleanstartup.com/
  Build-Measure-Learn loop; the story map must be editable without waste.

### Patterns for AI-ready workshops

- **Atlassian — How to run a remote workshop with Confluence + Jira** — https://www.atlassian.com/agile/project-management/workshops
  Industry template for workshop → backlog.

- **Miro Academy — AI in workshops** — https://help.miro.com/hc/en-us/categories/360002318013
  Canvas tagging and structuring patterns (analogous to FigJam).

---

## Source priority order

1. **Figma REST API** (technical — node structures) — https://www.figma.com/developers/api
2. **Anthropic Vision Guidelines** (prompt engineering) — https://docs.anthropic.com/en/docs/build-with-claude/vision
3. **tldraw / Make Real** (architecture reference) — https://github.com/tldraw/tldraw
4. **Patton (User Story Mapping)** (methodology) — https://www.jpattonassociates.com/user-story-mapping/

These four sources cover 90% of the guidelines. The rest is industry supplement.