---
name: step2-breadth-topic-suggester
version: 1.0.0
phase: 2
track: breadth
skill: beckmann-knowledge-graph-self-optimizer
description: Autonomous selection of a new breadth topic from overview and understanding report
author: Beckmann
license: MIT
tags: [knowledge-graph, topic-selection, breadth, ClawHub]
language: English
target: ClawHub
---

# Prompt Template — Step 2: Topic Selection (Breadth Track)

**Skill:** `beckmann-knowledge-graph-self-optimizer` v1.0.0  
**Template:** `Step2-Breadth-Topic-Suggester-Prompt-Template-V1.md`  
**Phase:** 2 — Breadth

---

## Purpose

This template is Phase 2 Breadth of the skill workflow. After the graph has been understood in Phase 1, it autonomously selects ONE new topic that expands the graph into a weakly represented area.

The selection is final and becomes the work order for Phase 3 (Subgraph Builder).

---

## Prerequisites

Per `SKILL.md` State Detection:

- `Results-and-Resources/graph_overview.json` present (from Phase 1a)
- `Results-and-Resources/UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` present (from Phase 1c)
- State = Phase 1 done → Phase 2

> This template uses only `graph_overview.json` + understanding report. Full `graph.json` is not needed.

---

## Inputs and Outputs

**Inputs (from `Results-and-Resources/`):**
- `graph_overview.json` — stats, typeHistogram, topPredicates, topHubs, bridgeCandidates, crossTypeConnections, entityIndex
- `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` — FORMAT, SUBGRAPHS, LOGIC, VALIDATION, Gaps

**Output (to `Results-and-Resources/`):**
- `Topic_Selection_Report_Breadth.txt` — autonomous final decision, English

State Detection after this step: `Topic_Selection_Report_*.txt` present → Gate 2→3

---

## Language Policy

- Template: English only
- Output report: English only
- No German, no prefixes

---

## THE PROMPT (Copy-paste ready)

```
You have systematically analyzed the knowledge graph in Phase 1. Your understanding report and overview are available. Now you execute Phase 2 Breadth: autonomous selection of a new topic for breadth growth.

KNOWLEDGE GRAPH OVERVIEW (JSON):
[[INSERT FULL graph_overview.json HERE]]

UNDERSTANDING REPORT FROM PHASE 1:
[[INSERT FULL UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md HERE]]

---

## YOUR TASK — Breadth

Select ONE topic autonomously. It will be expanded into a full subgraph in Phase 3. Save your result as Topic_Selection_Report_Breadth.txt.

### Definition — Breadth

A breadth theme expands the graph into an area that is currently not or only weakly represented:
- A type or domain has <8 entities in typeHistogram, OR
- The topic is only mentioned marginally in descriptions/entityIndex without a dedicated type cluster, OR
- It is identified as a Gap in UNDERSTANDING-REPORT Phase 4c
- The new type cluster does NOT already exist in typeHistogram

Use semantic type names only. No prefix codes.

### Procedure

**B1 — Identify candidates dynamically:**

Analyze graph_overview.json + understanding report for gaps:

- Which areas have <8 entities or are long-tail singletons in typeHistogram?
- Which Gaps are listed in understanding report Phase 4c?
- Which bridgeCandidates have weak connections to certain domains?
- Which scientific_status areas are underrepresented?
- What connection to core logic (Expectation, Simulation/Rendering, Reversal Effect, Security Principle, Dominant Expectation) is conceivable?

List at least 3 candidates with 2-3 sentence justification each, referencing concrete data (e.g., "type X has only 2 entities", "Gap Y from report").

**B2 — Select topic:**

Choose the candidate that:
(a) has strongest substantive relation to core logic (Dominant Expectation -> Reversal Effect -> Security Principle)
(b) does NOT exist as a type cluster in typeHistogram/entityIndex
(c) provides substance for >=10 new entities and >=5 new relations to existing entities
(d) addresses an explicit Gap and is not duplicate of existing caseStudies

Justify choice in 4-6 sentences, referencing TOTAL ASSESSMENT and specific gaps.

**B3 — Define new type cluster:**

- New Type Cluster / Domain: [2-5 words, English, not existing]
- Proposed new types (3-7 types that will belong to this cluster): [e.g., "Dominance Indicator", "Expectation Intensity", "Threshold Model"]
- Why this cluster does not duplicate an existing type: [check typeHistogram]
- Thematic fit: [how it fits to overall type system]

---

## SELF-CHECK (Mandatory before output)

[ ] Topic has no existing type cluster in graph_overview.json (checked typeHistogram + entityIndex)
[ ] At least 3 different existing entities (by id from entityIndex) that new subgraph could connect to
[ ] Proposed new types do not exist yet in graph_overview.json
[ ] Traceable relation to core logic (Expectation, Reversal Effect, Security Principle) — concrete, not generic

---

## OUTPUT FORMAT — Save as Topic_Selection_Report_Breadth.txt

TOPIC SELECTION REPORT — BREADTH — [[GRAPH_VERSION]]
Date: [[DATE]]
Created by: [[MODEL NAME]]

---

THEME — BREADTH

Title: [concise, 5-10 words, English]
New Type Cluster / Domain: [e.g., "Expectation Diagnostics"]
Proposed new types: [list 3-7]
Candidates Evaluated:
  1. [Title] — [2-3 sentence justification with typeHistogram count, Gap ID, bridgeCandidate]
  2. [Title] — [justification]
  3. [Title] — [justification]
Selected Theme: [Title]
Justification: [4-6 sentences, referencing TOTAL ASSESSMENT, Gaps, core logic — concrete]
Anchor Points in Existing Graph:
  - [id + type + how it could be connected]
  - [id + type + how it could be connected]
  - [id + type + how it could be connected]
Estimated Entity Count for New Subgraph: [>=10]
Estimated Relation Count: [>=5]
Connection to Next Phase: This report will be used as input for Step3-Subgraph-Builder-Prompt-Template-V1.md

---

SELF-CHECK RESULT:
[x] No existing type cluster — Confirmed: Checked typeHistogram, no cluster for...
[x] At least three anchors — Confirmed: Anchors are e.g., id1, id2, id3...
[x] New types do not exist — Confirmed: Checked types, proposed types are new...
[x] Traceable relation to core logic — Confirmed: ...
```

---

## Placeholder Replacement

| Placeholder | Content |
|---|---|
| `[[INSERT FULL graph_overview.json HERE]]` | Full `graph_overview.json` from `Results-and-Resources/` |
| `[[INSERT FULL UNDERSTANDING-REPORT-V3...]]` | Full report from Phase 1c |
| `[[GRAPH_VERSION]]` | e.g., "708 entities, 1179 relations" from overview |
| `[[DATE]]` | Execution date, e.g., 2026-09-19 |
| `[[MODEL NAME]]` | e.g., "Meta AI / Muse Spark 1.1" |

---

## What This Step Delivers

- Clearly defined breadth theme with New Type Cluster (no prefix)
- 3 concrete anchor points (verifiable ids from entityIndex)
- Autonomous decision saved as `Topic_Selection_Report_Breadth.txt`
- Direct input for Phase 3: `Topic_Selection_Report_Breadth.txt` + `graph_overview.json` + `UNDERSTANDING-REPORT-V3-...`

Gate 2→3 will review this report. Only (A) continues to Phase 3.

---

## Quality Check

A good `Topic_Selection_Report_Breadth.txt` has:

- **Breadth:** New type cluster has no predecessor in typeHistogram. Anchors are real existing ids from entityIndex. Count >=10 entities planned.
- **Concrete relation to core logic:** Not generic "has relation to expectations". Must be specific, e.g., "models how unconscious expectations shift game theory equilibria".
- **Dynamic derivation:** Candidates from overview (typeHistogram <8, long-tail, bridgeCandidates) + Gaps from understanding report. No static candidate list.
- **No prefixes:** Semantic types only.
- **English only**

---

## Next Steps (per SKILL.md)

1. Save output to `Results-and-Resources/Topic_Selection_Report_Breadth.txt`
2. SKILL.md detects Phase 2 done → shows Gate 2→3
3. After Gate (A): Phase 3 uses `Sub-Skills/Step3-Subgraph-Builder-Prompt-Template-V1.md` with this report as input

This file belongs to `Sub-Skills/` of `beckmann-knowledge-graph-self-optimizer` v1.0.0 and is published on ClawHub.
