---
name: pm-agent
description: AI-powered product management workflow agent. Use when the user wants to do product discovery, write PRDs, prioritize features, design experiments, plan launches, or run any PM workflow. Triggers on phrases like "product discovery", "write PRD", "user research", "prioritize features", "design sprint", "product launch", "opportunity mapping", "JTBD", "jobs to be done", "working backwards", "PM workflow", "product planning", "feature prioritization", "competitor analysis", "user persona", "GTM plan", "product strategy". Covers the full PM lifecycle from research to launch using proven frameworks (JTBD, Opportunity Solution Tree, RICE, Kano, Amazon Working Backwards, Google Design Sprint, Lean BML).
---

# PM Agent — AI Product Management Workflow

Four agents covering the full PM lifecycle: Research → Define → Validate → Launch. Each phase uses proven frameworks and produces structured artifacts. Human checkpoints between phases.

## Phases

| # | Phase | Agent | Framework | Output |
|---|-------|-------|-----------|--------|
| 1 | **Research** | Market & User Analyst | JTBD + Design Thinking | `DISCOVERY.md` |
| 2 | **Define** | Product Strategist | Opportunity Solution Tree + Amazon PRD | `PRD.md` |
| 3 | **Validate** | Experiment Designer | Design Sprint + Lean BML | `EXPERIMENT.md` |
| 4 | **Launch** | Go-to-Market Lead | Dual-Track Agile + OKR | `GTM.md` |

## How to Use

### Full Workflow

```
"I want to build [product idea]" → run all 4 phases
"Run pm-agent on [problem statement]"
```

Each phase spawns a focused subagent with the right prompt. The subagent asks questions, challenges assumptions, and produces a structured artifact.

### Partial Workflow

- "Just do a competitor analysis" → run Research only
- "Help me prioritize my backlog" → run Define (RICE/Kano section)
- "Write a PRD for this feature" → run Define with the feature description
- "Plan a design sprint" → run Validate only
- "Create a GTM plan" → run Launch only

### Single Commands

- `/research` — JTBD interview analysis, market sizing, competitive landscape
- `/define` — Opportunity Solution Tree, PRD with Amazon Working Backwards
- `/validate` — Experiment design, prototype testing plan, BML metrics
- `/launch` — GTM strategy, OKRs, release checklist

## Phase Details

### Phase 1: Research (JTBD + Design Thinking)

**Goal:** Understand the problem before proposing solutions.

Spawn a subagent (Sonnet) with the Research prompt from `references/prompts.md`. It will:

1. **JTBD Analysis** — Extract the "job" users are hiring the product for
   - Push factors (pain with current solution)
   - Pull factors (attraction of new solution)
   - Trigger event (what moment starts the search)
2. **Competitive Landscape** — Map existing solutions and gaps
3. **Market Sizing** — TAM/SAM/SOM with reasoning
4. **User Personas** — 2-3 evidence-based personas (not fictional)
5. **Write `DISCOVERY.md`** — Consolidated research artifact

**Key question:** "What job is the user hiring this product to do?"

### Phase 2: Define (Opp. Tree + Amazon PRD)

**Goal:** Define what to build and why, before how.

Spawn a subagent (Sonnet) with the Define prompt. It reads `DISCOVERY.md` and produces:

1. **Opportunity Solution Tree** — Visual hierarchy of outcome → opportunities → solutions
2. **Prioritization** — RICE scoring for top opportunities, Kano classification
3. **Amazon PRD** — Working Backwards: start with the press release, then FAQ
4. **User Stories** — INVEST-compliant stories with acceptance criteria
5. **Write `PRD.md`** — Complete product requirements document

**Key rule:** No solution before opportunity. No feature before user story.

### Phase 3: Validate (Design Sprint + Lean)

**Goal:** Test assumptions before building.

Spawn a subagent (Sonnet) with the Validate prompt. It reads `PRD.md` and produces:

1. **Assumption Map** — Classify by risk (lethality × uncertainty)
2. **Experiment Design** — Lean BML cycle for riskiest assumptions
3. **Prototype Plan** — What to mock up and how to test with 5 users
4. **Success Metrics** — Quantitative pass/fail criteria per experiment
5. **Write `EXPERIMENT.md`** — Validation plan with test scripts

**Key rule:** Test the riskiest assumption first, not the easiest.

### Phase 4: Launch (GTM + OKR)

**Goal:** Ship and measure.

Spawn a subagent (Haiku) with the Launch prompt. It reads `PRD.md` and `EXPERIMENT.md` and produces:

1. **GTM Strategy** — ICP, positioning, channel mix
2. **OKRs** — 3 measurable objectives with key results
3. **Release Checklist** — Pre-launch, launch day, post-launch tasks
4. **Feedback Loop** — How to collect and act on user signals
5. **Write `GTM.md`** — Launch plan with timelines

**Key rule:** Launch is not the end. It's the beginning of the BML cycle.

## Model Selection

| Phase | Model | Why |
|-------|-------|-----|
| Research | Sonnet | Needs reasoning for market analysis |
| Define | Sonnet | Strategic decisions require depth |
| Validate | Sonnet | Experiment design needs critical thinking |
| Launch | Haiku | Mostly structured execution |

## Output Files

All phase outputs go to the project root:

- `DISCOVERY.md` — Research findings (JTBD, personas, competitive landscape)
- `PRD.md` — Product requirements (Opp. Tree, Amazon PRD, user stories)
- `EXPERIMENT.md` — Validation plan (assumptions, experiments, metrics)
- `GTM.md` — Launch plan (GTM, OKRs, checklist)

Each file is self-contained but references previous phases. You can run phases independently by providing the prerequisite context.

## Frameworks Reference

For detailed framework guides (JTBD interview templates, RICE calculators, Amazon PRD templates), see `references/frameworks.md`.

## Human-in-the-Loop

Each phase ends with a checkpoint:

- **Approve** — proceed to next phase as-is
- **Edit** — modify the artifact, then proceed
- **Rerun** — provide feedback, regenerate the phase

This mirrors real PM work: AI drafts, humans decide.
