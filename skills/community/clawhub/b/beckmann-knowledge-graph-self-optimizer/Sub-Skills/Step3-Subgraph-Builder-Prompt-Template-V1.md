---
name: step3-subgraph-builder
version: 1.0.0
phase: 3
skill: beckmann-knowledge-graph-self-optimizer
description: Build a frozen subgraph with 10-20 entities and dual output for relation builder
author: Beckmann
license: MIT
tags: [knowledge-graph, subgraph-builder, validation, ClawHub]
language: English
target: ClawHub
---

# Prompt Template — Step 3: Subgraph Builder (Unified Breadth + Depth)

**Skill:** `beckmann-knowledge-graph-self-optimizer` v1.0.0  
**Template:** `Step3-Subgraph-Builder-Prompt-Template-V1.md`  
**Phase:** 3 — Subgraph Builder

---

## Purpose

Build a fully validated, isolated-displayable and directly mergeable subgraph with 10-20 entities (recommended 10-14) from a confirmed Topic Selection Report.

Unified for Breadth and Depth tracks. Validation is integrated — no external HTML validator.

---

## Prerequisites

Per `SKILL.md` State Detection and Gate 2→3:

- `Results-and-Resources/Topic_Selection_Report_Breadth.txt` OR `Topic_Selection_Report_Depth.txt` present after user review (A) Yes
- `Results-and-Resources/graph_overview.json` present
- `Results-and-Resources/UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` present

State must be Phase 2 done → Gate 2→3 passed.

---

## Inputs and Outputs

**Inputs (from `Results-and-Resources/`):**
- `Topic_Selection_Report_{Breadth|Depth}.txt` — after Gate 2→3, with Track, Title, Type Cluster / Deepening Focus, Proposed types, Anchor Points, Justification
- `graph_overview.json` — for duplicate check, entityIndex anchors, typeHistogram
- `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` — for core logic and gaps

**Outputs (to `Results-and-Resources/`, dual + protocol):**
1. `subgraph_breadth_new.json` OR `subgraph_depth_new.json` — final frozen subgraph, K1-K4 + J1-J4 + D1 valid, directly mergeable
2. `subgraph_breadth_new_information_for_Relation_Builder.json` OR `subgraph_depth_new_information_for_Relation_Builder.json` — transient bridge info for Phase 4, B1 + J3 valid
3. Final Protocol + STOP point (plain text, not JSON)

State after: both files present → Gate 3→4

---

## Language Policy

- Template: English only
- Output JSON and protocol: English only
- IDs: `snake_case`, no prefixes, English

---

## THEME — Unified Builder

**If Track == Breadth:**
New topic area. Type Cluster does NOT exist in typeHistogram. Subgraph opens a new field. Focus on important concepts, principles and causal mechanisms — structurally meaningful for core logic (Expectation, Reversal, Security, Dominant Expectation, Simulation/Rendering, Threshold, Calibration). Preferred internal predicates: `bridges`, `operationalizes`, `differentiates`, `causes`, `requires`.

**If Track == Depth:**
Explanatory intermediate layer between existing clusters. Existing Type Cluster DOES exist (>=10 entities but shallow, few cross-type connections). Operationalize / differentiate / causally explain. Preferred predicates: `causes`, `operationalizes`, `calibrates`, `instantiates`, `modulates`, `differentiates`.

Core rule: Use Topic Selection Report as work order — do not invent a new topic.

---

## Procedure S1: Parse Topic Selection Report (Mandatory First)

Extract exactly:

- Track: breadth | depth
- Title
- Type Cluster / Existing Type Cluster to Deepen
- Deepening Focus (Depth only)
- Proposed new types / subtypes: list 3-7
- Anchor Points: >=3 Breadth / >=5 Depth, thereof 3 same cluster for Depth, each with `id + type`
- Justification and Estimated Counts
- Self-Check from report

Verification S1-V:
- Check each Anchor ID exists in `graph_overview.json` entityIndex. If not, replace with nearest valid from bridgeCandidates, document replacement.
- Check typeHistogram: Breadth = Type Cluster NOT in histogram, Depth = DOES exist. Document for validation_snapshot.

S1 is internal reasoning, not emitted, but used for S2.

---

## Procedure S2: Planning Sketch BEFORE JSON (Mandatory)

Before any JSON, output a planning sketch in plain text (not JSON).

Format:

```
PLANNING SKETCH — [Track: breadth|depth] [Title]:
Core Node: [id you plan as hub — expected most connections]
Main Clusters (3-4):
  Cluster A: [Name] — [2-3 planned entity ids in this cluster]
  Cluster B: [Name] — [2-3 planned entity ids]
  Cluster C: [Name] — [2-3 planned entity ids]
  Cluster D (optional): [...]
Connections: [How A↔B↔C connect? e.g., A requires B, B modulates C, C operationalizes A]
[If Depth]: Connects main graph clusters [Cluster1 from report] ↔ [Cluster2 from report] deeper
Rationale: [Why this structure carries the topic? 2-3 sentences with core logic]
```

Rules:
- Core Node = node with most expected internal relations
- 3-4 clusters, each 2-4 entities
- No main-graph IDs in this sketch, only planned new ids
- Sketch must later match final subgraph or deviation justified

---

## Procedure S3: Generate 10-20 Entities

**K1:** 10-20 entities, recommended 10-14 for token economy.

Each entity MUST have exactly 3 fields:

- `id`: `snake_case`, e.g., `expectation_diagnostics`. Regex: `^[a-z]+(_[a-z0-9]+)+$`. Unique inside subgraph AND NOT existing in entityIndex.
- `type`: MUST be from Proposed types list from Topic Selection Report. No new type outside list without explicit justification.
- `description`: >=20 words, English, concrete, core-logic anchored. 1-4 sentences, relate to Expectation, Reversal, Security, Dominant Expectation, Simulation/Rendering, Threshold, Calibration, Operationalization. MUST NOT contain hard main-graph IDs after first word.

Forbidden:
- `scientific_status`, `label`, `connection_to_base_graph` fields
- Prefixes in id/type/description start
- Duplicate ids or collision with entityIndex

---

## Procedure S4: Generate Internal Relations — For File 1

**K2 — No isolated nodes:** Every entity has at least one relation to another new entity.

**K3 — Connected:** Whole subgraph connected — every node reachable from every other via relations.

**K4 — Self-contained:** Phase 3 builds subgraph WITHOUT connections to existing main graph. Every relation connects exclusively nodes of this new subgraph. Integration follows in Phase 4. File 1 contains ONLY internal relations.

Quantity:
- Breadth: >=5 internal relations
- Depth: >=8 internal relations

Each relation MUST have exactly 4 fields:

- `subject`: id of source entity (exact as in entities[].id)
- `predicate`: active verb phrase, snake_case, specific. Forbidden: `related_to`. Preferred: `requires`, `causes`, `operationalizes`, `differentiates`, `bridges`, `calibrates`, `instantiates`, `modulates`, `stabilizes`.
- `object`: id of target entity (exact as in entities[].id)
- `description`: >=15 words, causal justification, 1-3 sentences.

Forbidden: self-loops, duplicates, `related_to`, external ids.

---

## Procedure S5: Integrated Validation — J1-J4 + D1 + B1 + K1-K4

LLM must perform ALL checks internally BEFORE emitting outputs. If any fails, repair internally then re-validate.

**J1 — Syntax:**
- All braces have closing counterparts
- All strings in double quotes, commas between fields, no trailing commas
- Valid JSON parseable

**J2 — Completeness:**
- Every entity has `id`, `type`, `description`?
- Every relation has `subject`, `predicate`, `object`, `description`?
- entity_count >=10 and <=20?
- internal relation count >=5 Breadth / >=8 Depth?

**J3 — Referential Integrity (critical):**
1. List all new entity IDs from File 1
2. Check every internal relation: subject ∈ list? object ∈ list?
3. For File 2: Check every `object_existing` ∈ graph_overview.json entityIndex
4. Error format: `ERROR J3: '[missing ID]' not in entities.` / `ERROR J3: '[anchor ID]' not in entityIndex.`

**J4 — ID Consistency:**
- All id, type, predicate follow snake_case regex?
- No id collides with entityIndex?
- No prefix pattern?

**D1 — ID Hygiene:**
- Search all description fields after first word for patterns that look like main-graph IDs
- After first word, no hard ID from entityIndex may appear. Mention other entities only by descriptive name.
- Example WRONG: "This complements dominant_expectation_v2"
- Example CORRECT: "This complements the security principle by..."

**B1 — Anchor Points (for File 2):**
- File 2 `proposed_bridge_relations` >=3 Breadth / >=5 Depth. If not: WARNING B1.

**K1-K4 — Structure:**
- K1: 10-20 nodes?
- K2: no isolated?
- K3: connected?
- K4: only internal in File 1?

Additional:
- typeHistogram check passed?
- description length >=20 entities / >=15 relations?
- No `related_to`?
- File 1 directly mergeable (entities + relations arrays, no wrapper, no external refs)?
- Planning sketch matches final subgraph?

Validation output format (mandatory):

```
VALIDATION JSON — [Track] [Title]:
J1 Syntax:               [ ✓ / ✗ Error: ... ]
J2 Required Fields:      [ ✓ / ✗ Error: ... ]
J3 Referential:          [ ✓ / ✗ Error: ... ]
J4 ID Consistency:       [ ✓ / ✗ Error: ... ]
D1 ID Hygiene:           [ ✓ / ✗ Error: ... ]
B1 Anchors:              [ ✓ / ✗ — n bridges in File 2 ]
K1-K4 Structure:         [ ✓ / ✗ — K1:..., K2:..., K3:..., K4:... ]
typeHistogram:           [ ✓ / ✗ ]
description length:      [ ✓ / ✗ ]
```

If any ✗, repair before emitting.

---

## Procedure S6: Dual-Output Generation + Final Protocol

Emit in exact order:

1. PLANNING SKETCH (from S2, plain text)
2. VALIDATION JSON — [Track] (from S5, plain text)
3. File 1 JSON code block with filename comment
4. File 2 JSON code block with filename comment
5. FINAL PROTOCOL + STOP POINT (plain text)

### Output File 1 — Final Subgraph

Filename: `subgraph_breadth_new.json` OR `subgraph_depth_new.json`

Schema:

```json
{
  "entities": [
    {
      "id": "text",
      "type": "text",
      "description": "text"
    }
  ],
  "relations": [
    {
      "subject": "text",
      "predicate": "text",
      "object": "text",
      "description": "text"
    }
  ]
}
```

Rules: 10-20 entities (10-14 recommended), only internal relations, K2-K3 satisfied, J1-J4 ✓, D1 ✓, isolated displayable and directly mergeable.

### Output File 2 — Information for Relation Builder (transient)

Filename: `subgraph_breadth_new_information_for_Relation_Builder.json` OR `subgraph_depth_new_information_for_Relation_Builder.json`

Purpose: Everything Phase 4 needs to build bridge relations. Will be deleted after Phase 4.

Schema:

```json
{
  "source_track": "breadth | depth",
  "topic_title": "Title from Topic Selection Report",
  "type_cluster": "Type Cluster from Report",
  "proposed_types": ["type1", "type2"],
  "new_entity_ids": ["id1", "id2"],
  "anchor_points_verified": [
    {
      "id": "existing_entity_id_from_entityIndex",
      "type": "type_from_overview",
      "role": "bridge_target | differentiation_base | operationalization_base"
    }
  ],
  "proposed_bridge_relations": [
    {
      "subject_new": "id_from_new_subgraph",
      "predicate": "bridges | operationalizes | differentiates | causes | calibrates | instantiates | modulates",
      "object_existing": "id_from_entityIndex",
      "rationale": "Connects to 'Label' (object_existing) through [type of connection]. [Explanation 1-2 sentences with core logic].",
      "anchor_verification": "exists_in_entityIndex_true"
    }
  ],
  "phase4_hints": {
    "expected_bridge_count": 3,
    "forbidden_predicates": ["related_to"],
    "preferred_predicates": ["operationalizes", "differentiates", "causes", "bridges", "calibrates"],
    "justification_summary": "summary from Topic Selection Report",
    "planning_sketch_reference": "copy of planning sketch from S2"
  },
  "validation_snapshot": {
    "entity_count": 10,
    "internal_relation_count": 6,
    "all_ids_unique": true,
    "all_anchors_exist": true,
    "typeHistogram_check_passed": true,
    "j1_j4_passed": true,
    "d1_passed": true,
    "b1_count": 4,
    "k1_k4_passed": true
  }
}
```

Rules:
- No duplicate entities/relations from File 1, only IDs
- All `object_existing` MUST exist in entityIndex (J3)
- At least 3 bridges Breadth, 5 bridges Depth (B1)
- `anchor_verification` must be `exists_in_entityIndex_true`
- Consumed in Phase 4 by `Step4-Relation-Builder-Prompt-Template-V3.md`

### Final Protocol + STOP POINT (mandatory, plain text)

```
FINAL PROTOCOL PHASE 3 — CYCLE [n] — [Breadth|Depth]
Date: [YYYY-MM-DD]
Model: [AI model and version]
Track: [breadth|depth]
Topic: [Title from Topic Selection Report]
-----------------------------------------
Subgraph:
  File:              subgraph_[breadth|depth]_new.json
  Nodes:             [count] (K1: 10-20, rec. 10-14)
  Relations internal:[count] (>=5 Breadth / >=8 Depth)
  Planning Sketch:   present ✓ / missing ✗
  Connected:         yes/no (K3)

Bridge Info (transient):
  File:              subgraph_[breadth|depth]_new_information_for_Relation_Builder.json
  Anchors:           [count] bridges (B1: >=3/>=5)
  Anchors verified:  yes/no (all in entityIndex, J3)

Validations:
  J1 Syntax:               [ ✓ / ✗ ]
  J2 Required Fields:      [ ✓ / ✗ ]
  J3 Referential:          [ ✓ / ✗ ]
  J4 ID Consistency:       [ ✓ / ✗ ]
  D1 ID Hygiene:           [ ✓ / ✗ ]
  B1 Anchors:              [ ✓ / ✗ ]
  K1-K4 Structure:         [ ✓ / ✗ ]
  typeHistogram:           [ ✓ / ✗ ]
-----------------------------------------
STOP POINT:
Phase 3 is complete. The subgraph is ready for human review.

Only after explicit human approval may Phase 4 (relations to main graph) continue.

Possible next steps:
  (1) Human review and approval → continue with Phase 4
  (2) Discard subgraph → start new cycle
  (3) Correct subgraph → re-run Step3 prompt

Phase 3 gives no recommendation. Decision lies with human.
```

---

## Self-Check — Must pass before emitting

```
- [ ] Planning Sketch present before JSON (S2) — matches graph or deviation justified
- [ ] File 1: 10-20 entities (K1), rec. 10-14
- [ ] File 1: K2 no isolated, K3 connected, K4 only internal relations
- [ ] File 1: Schema = {entities:[{id,type,description}], relations:[{subject,predicate,object,description}]}
- [ ] File 1: All ids snake_case, unique, not in entityIndex
- [ ] File 1: J1-J4 ✓, D1 ✓
- [ ] File 2: All anchors verified in entityIndex (J3) — anchor_verification = exists_in_entityIndex_true
- [ ] File 2: B1 >=3 Breadth / >=5 Depth, rationale present
- [ ] File 2: No related_to, only preferred predicates
- [ ] Both files valid JSON (J1)
- [ ] Final Protocol + STOP POINT present with all ✓
- [ ] No full graph.json read, only graph_overview.json
```

---

## Security Rules

1. **No autoloop:** Phase 3 always ends at STOP point. Merge into main graph (Phase 4/5) is separate.
2. **No version number by model:** Filename contains only track + new, never version number of combined graph. Versioning is done by human.
3. **Main graph untouched:** Phase 3 does not modify main graph. Only reads graph_overview.json.
4. **Human approval before Phase 4:** Decision always lies with human.

---

## Anti-Patterns

- Do not read full graph.json — only overview + reports, otherwise token overflow
- Do not hallucinate anchor IDs in File 1 — File 1 only new IDs, existing IDs only in File 2 as object_existing
- Do not use `related_to` — use `operationalizes`, `differentiates`, `causes`, `bridges`, `calibrates`, `instantiates`, `modulates`
- No prefix patterns — only snake_case
- No duplicate to typeHistogram — check before, document in snapshot
- Description too short / encyclopedic — min 20 words entities, 15 words relations, concrete, core-logic anchored
- Do not mix File 1 and File 2 — File 1 = internal world (K4), File 2 = bridge world
- Do not skip planning sketch — mandatory
- Do not place IDs in middle of description — D1 violation — after first word no ID patterns
- Do not skip self-check — mandatory

---

## Output Order Summary

```
── S1: PARSE TOPIC REPORT (internal) ────────
Track: [...], Title: [...], Type Cluster: [...], Anchors: [...]

── S2: PLANNING SKETCH — [Track] [Title] ──
Core Node: [...]
Main Clusters (3-4): [...]
Connections: [...]
[Depth]: Connects main graph clusters [A] ↔ [B]
Rationale: [...]

── S3+S4: SUBGRAPH (File 1) ────────────────
{ "entities": [...], "relations": [...] }

VALIDATION JSON — [Track] [Title]:
J1... J4... D1... B1... K1-K4...

── File 2: BRIDGE INFO ────────────────────
{ "new_entity_ids": [...], "anchor_points_verified": [...], "proposed_bridge_relations": [...] }

── S6: FINAL ──────────────────────────────
FINAL PROTOCOL PHASE 3 — CYCLE [n]
[...]
STOP POINT
```

---

## Placeholder Overview

| Placeholder | Content |
|---|---|
| `Topic_Selection_Report_{Breadth\|Depth}.txt` | Output from Phase 2 after Gate 2→3 (A) Yes |
| `graph_overview.json` | Output from Graph-Overview-Generator, from `Results-and-Resources/` |
| `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` | Output from Phase 1c |

---

## Next Steps (per SKILL.md)

After this template succeeds and both files are in `Results-and-Resources/`:

1. SKILL.md detects Phase 3 done → shows Gate 3→4
2. After Gate (A): Phase 4 uses `Sub-Skills/Step4-Relation-Builder-Prompt-Template-V3.md` with both files as input

This file belongs to `Sub-Skills/` of `beckmann-knowledge-graph-self-optimizer` v1.0.0 and is published on ClawHub.
