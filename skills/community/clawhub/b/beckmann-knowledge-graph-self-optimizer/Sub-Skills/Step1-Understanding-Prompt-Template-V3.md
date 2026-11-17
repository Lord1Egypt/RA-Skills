---
name: step1-understanding-prompt-template
version: 4.0.0
phase: 1c
skill: beckmann-knowledge-graph-self-optimizer
description: Systematic understanding of a knowledge graph from overview and split parts — generates UNDERSTANDING-REPORT
author: Beckmann
license: MIT
tags: [knowledge-graph, understanding, analysis, overview, ClawHub]
language: English
target: ClawHub
---

# Prompt Template — Step 1c: Understanding the Knowledge Graph

**Skill:** `beckmann-knowledge-graph-self-optimizer` (v1.0.1)  
**Template Version:** 4.0.0 — 2026-09-19 — ClawHub-ready / English  
**Replaces:** `Step1-Understanding-Prompt-Template-V3.md`

---

## Purpose

This is Phase 1c of the skill workflow. It forces any LLM to systematically understand the full knowledge graph **before** any extension is allowed.

It is used **after** Phase 1a and 1b are completed by the user. It takes the outputs of the HTML tools and produces the foundation for all later phases (Topic Selection, Subgraph Builder, Relation Builder).

Use this template as a copy-paste prompt in a new AI session.

---

## Prerequisites (must be completed via SKILL.md)

Per `SKILL.md` Startup Behavior and Phase 1:

1. `Results-and-Resources/graph.json` placed by user
2. Phase 1a: `HTML-Tools/Graph-Overview-Generator.html` → `Results-and-Resources/graph_overview.json`
3. Phase 1b: `HTML-Tools/Knowledge-Graph-Splitter.html` → `Results-and-Resources/graph_Part_1_of_4.json` … `graph_Part_4_of_4.json`

> HTML tools are client-side, offline, user-operated. No data is sent externally. The agent only instructs and waits for file presence.

If `graph_overview.json` or the 4 part files are missing, **stop** and ask the user to run Phase 1a / 1b first. Do not attempt to analyze raw `graph.json` directly in this phase.

---

## Inputs and Outputs

**Inputs (from `Results-and-Resources/`):**
- `graph_overview.json` — from `Graph-Overview-Generator.html`
- `graph_Part_1_of_4.json`
- `graph_Part_2_of_4.json`
- `graph_Part_3_of_4.json`
- `graph_Part_4_of_4.json`

Each part file contains a `_meta` field with traceability:
```json
"_meta": {
  "source": "graph.json",
  "segment": "Part_1_of_4",
  "segment_index": 1,
  "segment_total": 4
}
```

**Output (to `Results-and-Resources/`):**
- `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md`

> Note for V1.0 compatibility: SKILL.md v1.0.0 state detection expects exactly this filename. This V4 template still generates the V3-named file. In a future skill release the filename will be renamed to `UNDERSTANDING-REPORT-V4-...`. Keep the V3 name for now.

---

## Language Policy

- This template: English only
- Output report: English only
- Relation content (`predicate`, `description`) in later phases: English only
- No German, no mixed language

---

## THE PROMPT (Copy-paste ready)

```
You receive a knowledge graph split into 4 parts plus an overview. Your task is to systematically understand the FULL graph and produce ONE consolidated UNDERSTANDING REPORT.

You must process all 4 parts sequentially and accumulate results. Do NOT produce 4 partial reports — produce ONE final report at the end.

---
INPUT FILES — attached by user from Results-and-Resources/:
1. graph_overview.json
2. graph_Part_1_of_4.json
3. graph_Part_2_of_4.json
4. graph_Part_3_of_4.json
5. graph_Part_4_of_4.json
---

## PHASE 1 — Format & Data Structure

Describe the JSON format precisely:

1. Top-level fields: e.g., _meta, entities, relations, nodes, edges
2. Entity fields: Which are present in ALL entities, which are optional? Check: id, type, description, scientific_status, comment, tags, etc.
3. Relation fields: Which are present in ALL relations, which are optional? Check: subject/source/from, predicate/relation/type, object/target/to, description, scientific_status, etc.
4. Total counts: entities and relations across all 4 parts (sum _meta if needed)
5. _meta content: What does overview and part _meta contain?

Output Phase 1:
- Prose, max 150 words
- No bullet lists, no tables
- Write as if explaining to a new colleague

---

## PHASE 2 — Subgraph Mapping & Clusters

Current graph uses `type` field and relation density for clustering. Old prefix system (E1, G4) is DEPRECATED — do not use it.

Perform:

1. Extract all unique `type` values. Table:
   | Type | Entity Count | Example Entities (2-3 ids) | Theme derived by you |

2. Hub Structure:
   - Calculate degree (incoming + outgoing relations) per entity across all parts
   - List Top 10 Hub Entities: id, type, degree, 1-sentence role
   - Which type(s) contain the most hubs?

3. Bridge Nodes:
   Definition: Entity whose relations link to >=3 different target types, OR Top 20 by degree AND connects to >=2 types
   - List all bridge nodes: id, degree, connected types, why it bridges

4. Cluster Connectivity:
   - Which three type-clusters are most strongly interconnected (by cross-type relation count)?

5. Optional Domain Check (only if present):
   If entities like "Reversal Effect", "Security Principle" etc. exist, map which type cluster they belong to. If not present, write "Not applicable to this graph."

---

## PHASE 3 — Logic & Patterns

### 3a — Hub Entities
Describe Top 3 Hubs in detail:
- Role in graph?
- Why central (incoming vs outgoing)?

### 3b — Argumentation Chains
Find 3-5 chains: A -> (predicate) -> B -> (predicate) -> C ...
Min 3 nodes each, at least one chain must cross type boundaries.
Describe chain and logical statement it makes.

### 3c — Predicate Patterns
Top 3 most frequent predicates. What does dominance tell about graph logic (causal, hierarchical, associative)?

### 3d — Core Theses
Formulate 3-5 core theses the graph makes as a whole, in your own words. Support each with >=2 concrete entities or relations.

---

## PHASE 4 — Validation & Protocol

### 4a — Comprehension Test (answer from graph only)

Q1: What are the 2-3 most central concepts by degree, and why central?
Q2: Which type cluster appears to describe case studies / historical examples / comments, if any? What do those entities have in common?
Q3: What does `scientific_status` indicate if present? Distribution? If not present, what alternative quality indicator is used?

### 4b — Integration Test
If a new node "[[NEW TEST NODE]]" should be added:
- Which type would it belong to?
- Which 3 existing entities would it likely reference?
- Which predicate would its most important relation have?
- Justify from graph logic.

### 4c — Gaps & Inconsistencies
List 2-3 gaps (topic hinted by several entities but never own entity) and 2-3 structural inconsistencies (contradicting predicate, missing required field).

---

## OUTPUT FORMAT (Mandatory — follow exactly)

UNDERSTANDING REPORT — [[GRAPH-VERSION]]
Date: [[CURRENT DATE]]
Created by: [[AI MODEL NAME AND VERSION]]
Source: graph_Part_1_of_4.json … graph_Part_4_of_4.json + graph_overview.json (4 parts)
Tool: HTML-Tools/Graph-Overview-Generator.html + HTML-Tools/Knowledge-Graph-Splitter.html

PHASE 1 — FORMAT
[your answer]

PHASE 2 — SUBGRAPHS
[your answer incl. type table and bridge node list]

PHASE 3 — LOGIC
3a Hub Entities: [...]
3b Chains: [...]
3c Predicate Patterns: [...]
3d Core Theses: [...]

PHASE 4 — VALIDATION
4a Comprehension Test: [...]
4b Integration Test: [...]
4c Gaps: [...]

TOTAL ASSESSMENT:
Coherence (1-5): [score] — 1=many contradictions, 5=fully coherent
Justification: [2-3 sentences]
Processing Mode: Segmented Mode — 4 segments × ~[[AVG ENTITIES]] entities (from HTML-Tools)
Entity Count: [[TOTAL]]
Relation Count: [[TOTAL]]
Types: [[LIST]]

---
Important: Use ONLY information contained in the provided files. Do not add from prior knowledge. If not derivable, write: "Not derivable from graph."
```

---

## Placeholder Replacement

| Placeholder | Replacement |
|---|---|
| `[[GRAPH-VERSION]]` | From `graph_overview.json` _meta or "current main" |
| `[[CURRENT DATE]]` | Execution date, e.g., 2026-09-19 |
| `[[AI MODEL NAME AND VERSION]]` | e.g., "Meta AI / Muse Spark 1.1" |
| `[[NEW TEST NODE]]` | Provide a hypothetical node to test integration, e.g., "External Reality Check 2.0" |
| `[[TOTAL]]`, `[[LIST]]`, `[[AVG ENTITIES]]` | Fill from actual counts |

---

## What This Step Delivers

- Type logic correctly understood (prerequisite for Phase 2 Topic Selection)
- Bridge nodes identified (prerequisite for Phase 3 Subgraph Builder — anchor requirement B1 >=3)
- Hub entities known (prerequisite for Phase 4 Relation Builder)
- Gaps documented (input for Breadth vs Depth decision)

The output report is read by `SKILL.md` State Detection: if present and no Topic Report yet, state = Phase 1 done → start Phase 2.

---

## Quality Check (for reviewers and Gate 2→3)

A good report must:

- List ALL `type` values with correct counts (not invented)
- Calculate hubs by actual degree (sum across 4 parts), not guessing
- Describe >=1 cross-type argumentation chain
- Identify `scientific_status` or alternative quality field if present
- List `anmerkung_*` or `connection_to_base_graph` as meta-layer if they exist
- Does NOT use old prefix system (E1, G4) as if still active
- Clearly states `Processing Mode: Segmented Mode — 4 segments`
- Is English only

If any check fails, request revision before Gate 2→3.

---

## Tooling Reference

- `HTML-Tools/Graph-Overview-Generator.html` — generates `graph_overview.json`
- `HTML-Tools/Knowledge-Graph-Splitter.html` — generates 4 parts, modes: By count (recommended 4 segments for ~80-120 entities per segment), By size, By type
- Both tools are generic: support `entities/relations`, `nodes/edges`, `nodes/links`, plain arrays
- Located in `HTML-Tools/` folder of the skill

---

## Versioning

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-05-18 | Initial, German, prefix-based, aligned to Graph V151 |
| 1.1 | 2026-06-19 | Size-check A-D added, output mode tracking |
| 1.2 | 2026-06-25 | Model-agnostic prep: AI proposes split, user executes via HTML |
| 3.0 | 2026-09-06 | Major rewrite: English, ClawHub-ready, generic for any KG, prefix deprecated → type-based, compatible with Knowledge-Graph-Splitter v2 |
| 4.0 | 2026-09-19 | ClawHub V1.0 alignment: frontmatter added, prerequisites aligned to SKILL.md Phase 1a/1b, inputs fixed to graph_overview.json + 4 parts, old size-check proposal removed, folder renamed to Results-and-Resources, HTML tool names fixed to hyphen versions, output filename kept V3 for state-detection compatibility, language policy clarified |
| 4.0.1 | 2026-09-21 | Tool reference updated: KnowledgeGraph-Splitter.html → Knowledge-Graph-Splitter.html (V1.0.1 rename) |

---

## Next Steps in Skill Workflow (per SKILL.md)

After this template succeeds and `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` is in `Results-and-Resources/`:

1. SKILL.md detects Phase 1 done → starts Phase 2
2. Phase 2: Use `Step2-Breadth-Topic-Suggester-Prompt-Template-V1.md` or `Step2-Depth-...`
3. Continue with Gate 2→3 → Phase 3 → Gate 3→4 → Phase 4 → Gate 4→5 → Phase 5

This file belongs to `Sub-Skills/` folder of `beckmann-knowledge-graph-self-optimizer` and is published on ClawHub as part of skill v1.0.1.
