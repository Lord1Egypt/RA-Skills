---
name: step2-depth-topic-suggester
version: 1.0.0
phase: 2
track: depth
skill: beckmann-knowledge-graph-self-optimizer
description: Autonomous selection of an existing topic cluster for depth growth
author: Beckmann
license: MIT
tags: [knowledge-graph, topic-selection, depth, ClawHub]
language: English
target: ClawHub
---

# Prompt Template — Step 2: Topic Selection (Depth Track)

**Skill:** `beckmann-knowledge-graph-self-optimizer` v1.0.0  
**Template:** `Step2-Depth-Topic-Suggester-Prompt-Template-V1.md`  
**Phase:** 2 — Depth

---

## Purpose

This template is Phase 2 Depth of the skill workflow. After the graph has been understood in Phase 1, it autonomously selects ONE existing topic cluster that is strongly represented but shallow and needs deepening.

It is the structural twin of the Breadth template with inverted logic. The selection is final and becomes the work order for Phase 3 (Subgraph Builder).

---

## Prerequisites

Per `SKILL.md` State Detection:

- `Results-and-Resources/graph_overview.json` present (from Phase 1a)
- `Results-and-Resources/UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` present (from Phase 1c)
- State = Phase 1 done → Phase 2

> Uses only `graph_overview.json` + understanding report. Full `graph.json` is not needed.

---

## Inputs and Outputs

**Inputs (from `Results-and-Resources/`):**
- `graph_overview.json` — stats, typeHistogram, topPredicates, topHubs, bridgeCandidates, crossTypeConnections, entityIndex
- `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` — FORMAT, SUBGRAPHS, LOGIC, VALIDATION, Gaps

**Output (to `Results-and-Resources/`):**
- `Topic_Selection_Report_Depth.txt` — autonomous final decision, English

State Detection after this step: `Topic_Selection_Report_*.txt` present → Gate 2→3

---

## Language Policy

- Template: English only
- Output report: English only
- No German, no prefixes

---

## THE PROMPT (Copy-paste ready)

```
You have systematically analyzed the knowledge graph in Phase 1. Your understanding report and overview are available. Now you execute Phase 2 Depth: autonomous selection of an EXISTING topic for depth growth.

KNOWLEDGE GRAPH OVERVIEW (JSON):
[[INSERT FULL graph_overview.json HERE]]

UNDERSTANDING REPORT FROM PHASE 1:
[[INSERT FULL UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md HERE]]

---

## YOUR TASK — Depth

Select ONE existing topic cluster autonomously for DEEPENING. It will be expanded with additional entities, mechanisms and relations in Phase 3. Save as Topic_Selection_Report_Depth.txt. This is NOT a new field — it deepens what already exists.

### Definition — Depth

A depth theme deepens an area that IS strongly represented but shallow, under-connected or lacks operationalization:
- A type cluster has >=10 entities in typeHistogram (ideally 15-30) but low crossTypeConnections or low predicate diversity, OR
- A bridgeCandidate has high type diversity but few actual bridging relations to other domains, OR
- The cluster is identified as a Gap in UNDERSTANDING-REPORT Phase 4c (e.g., missing quantitative threshold, missing causal chains, taxonomy fragmentation), OR
- The cluster has high metaphor/hypothesis vs low established/empirical status inside the same dense area, OR
- An existing caseStudy is present but lacks mechanistic depth
- The existing type cluster DOES already exist in typeHistogram — inverse to Breadth

Use semantic type names only. Depth elaborates existing clusters, does not invent new top-level clusters.

### Procedure

**D1 — Identify candidates dynamically:**

Analyze graph_overview.json + understanding report for deepening needs:

- Which type clusters have >=10 entities but <5 crossTypeConnections or low predicate diversity? Check topHubs for many incoming relations but missing mechanistic elaboration.
- Which bridgeCandidates have high type diversity but weak actual bridging relations?
- Which Gaps are listed in Phase 4c? (e.g., taxonomy fragmentation → consolidation, missing threshold → operationalization, collective vs individual not distinguished → differentiation, missing causal chains)
- Which scientific_status areas are overrepresented as metaphor/hypothesis inside a dense cluster?
- Which caseStudies could be deepened with mechanisms, measurements or threshold models?
- What connection to core logic (Expectation, Simulation/Rendering, Reversal Effect, Security Principle, Dominant Expectation) would remain incomplete WITHOUT this deepening?

List at least 3 candidates with 2-3 sentence justification each, referencing concrete data (e.g., "type X has 22 entities but only 3 crossTypeConnections").

**D2 — Select topic:**

Choose the candidate that:
(a) has strongest substantive relation to core logic that remains INCOMPLETE without deepening
(b) DOES exist as type cluster in typeHistogram with >=10 entities (must exist, inverse to Breadth)
(c) provides substance for >=10 new entities deepening the existing cluster and >=8 new relations (causal, operationalizing, bridging, differentiating)
(d) addresses an explicit Gap and deepens rather than duplicates existing caseStudies

Justify choice in 4-6 sentences, referencing TOTAL ASSESSMENT and specific gaps. Explain why without this deepening the core logic stays unoperationalized.

**D3 — Define deepening:**

- Existing Type Cluster / Domain to Deepen: [e.g., "Reversal Effect" — must exist with >=10 entities]
- Deepening Focus: [e.g., "Threshold Operationalization and Collective vs Individual Differentiation" — 3-7 words, specific mechanism]
- Proposed new subtypes / aspects / mechanisms (3-7 types that elaborate existing cluster): [e.g., "Threshold Model", "Collective Reversal Indicator", "Security Deactivation Condition"]
- Why this deepening does not duplicate but elaborates: [check typeHistogram — proposed subtypes are new but plausible children of existing cluster]
- Thematic fit: [how deepening resolves Gap and strengthens core chain]

---

## SELF-CHECK (Mandatory before output)

[ ] Topic HAS existing type cluster in graph_overview.json (>=10 checked, exists)
[ ] At least five different existing entities (by id from entityIndex), at least 3 from same existing cluster, for deepening to attach to
[ ] Proposed new subtypes / mechanisms do NOT exist yet as types, but are plausible elaborations of existing cluster
[ ] Traceable relation to core logic — concrete mechanism, not generic
[ ] Estimated relations >=8, justified by need for causal / operationalizing / bridging / differentiating relations

---

## OUTPUT FORMAT — Save as Topic_Selection_Report_Depth.txt

TOPIC SELECTION REPORT — DEPTH — [[GRAPH_VERSION]]
Date: [[DATE]]
Created by: [[MODEL NAME]]

---

THEME — DEPTH

Title: [concise, 5-10 words, English]
Existing Type Cluster / Domain to Deepen: [must exist, >=10 entities, e.g., "Reversal Effect"]
Deepening Focus: [e.g., "Threshold Operationalization and Collective Differentiation"]
Proposed new subtypes / aspects: [list 3-7]
Candidates Evaluated:
  1. [Title] — [2-3 sentence justification with typeHistogram >=10, low crossTypeConnections, Gap ID, bridgeCandidate]
  2. [Title] — [justification]
  3. [Title] — [justification]
Selected Theme: [Title]
Justification: [4-6 sentences, referencing TOTAL ASSESSMENT, Gaps, core logic — concrete]
Anchor Points in Existing Graph:
  - [id + type + how deepening connects — same cluster]
  - [id + type + connection — same cluster]
  - [id + type + connection — same cluster]
  - [id + type + connection — bridging, e.g., dominant expectation]
  - [id + type + connection — bridging, e.g., security principle]
Estimated Entity Count for New Subgraph: [>=10]
Estimated Relation Count: [>=8 — Depth requires denser networking]
Connection to Next Phase: This report will be used as input for Step3-Subgraph-Builder-Prompt-Template-V1.md

---

SELF-CHECK RESULT:
[x] HAS existing type cluster — Confirmed: Checked typeHistogram, cluster exists with X entities...
[x] At least five anchors (3 same cluster) — Confirmed: Anchors are...
[x] New subtypes elaborate, not duplicate — Confirmed: Proposed subtypes are new operationalizations...
[x] Traceable relation to core logic — Confirmed: Deepening operationalizes...
[x] Estimated relations >=8 — Confirmed: Needs causal + operationalizing + bridging + differentiating...
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

- Clearly defined existing theme to deepen (HAS existing type cluster >=10, inverse to Breadth)
- Deepening Focus + 3-7 new subtypes / mechanisms / operationalizations inside existing cluster
- 5 concrete anchor points (verifiable ids from entityIndex), at least 3 from same cluster
- Autonomous decision saved as `Topic_Selection_Report_Depth.txt`
- Direct input for Phase 3: `Topic_Selection_Report_Depth.txt` + `graph_overview.json` + `UNDERSTANDING-REPORT-V3-...`

Gate 2→3 will review this report. Only (A) continues to Phase 3.

---

## Quality Check

A good `Topic_Selection_Report_Depth.txt` has:

- **Depth:** Existing cluster DOES exist with >=10 entities. Low crossTypeConnections or high metaphor/hypothesis status or missing causal chain. Anchors real existing ids, >=5 with >=3 from same cluster. Planned >=10 entities, >=8 relations.
- **Concrete core logic:** Not generic "has relation to reversal". Must be specific, e.g., "operationalizes quantitative threshold at which dominant expectation triggers reversal and deactivates security principle".
- **Dynamic derivation:** Candidates from overview (>=10 + low crossTypeConnections + topHubs + bridgeCandidates high diversity but weak bridging + scientific_status metaphor-heavy) + Gaps from report. No static list.
- **No prefixes:** Semantic types only. Depth elaborates, does not invent new top-level prefix.
- **Inverse to Breadth:** Breadth = new cluster does NOT exist. Depth = existing cluster DOES exist and is deepened.
- **English only**

---

## Next Steps (per SKILL.md)

1. Save output to `Results-and-Resources/Topic_Selection_Report_Depth.txt`
2. SKILL.md detects Phase 2 done → shows Gate 2→3
3. After Gate (A): Phase 3 uses `Sub-Skills/Step3-Subgraph-Builder-Prompt-Template-V1.md` with this report as input

This file belongs to `Sub-Skills/` of `beckmann-knowledge-graph-self-optimizer` v1.0.0 and is published on ClawHub.
