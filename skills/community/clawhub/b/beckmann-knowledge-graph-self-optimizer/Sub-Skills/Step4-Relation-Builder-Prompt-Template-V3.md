---
name: step4-relation-builder
version: 3.0.0
phase: 4
skill: beckmann-knowledge-graph-self-optimizer
description: Build bridge relations from frozen subgraph to existing graph — directly mergeable
author: Beckmann
license: MIT
tags: [knowledge-graph, relation-builder, bridge-relations, ClawHub]
language: English
target: ClawHub
---

# Prompt Template — Step 4: Relation Builder (Bridge Building)

**Skill:** `beckmann-knowledge-graph-self-optimizer` v1.0.0  
**Template:** `Step4-Relation-Builder-Prompt-Template-V3.md`  
**Phase:** 4 — Relation Builder

---

## Purpose

Phase 4 generates the final, directly mergeable bridge relations from the frozen subgraph (Phase 3) to the existing main graph.

Unified for Breadth and Depth tracks. Output is rationale-free JSON (4 fields) that can be merged in Phase 5 without further transformation.

---

## Prerequisites

Per `SKILL.md` State Detection and Gate 3→4:

- `Results-and-Resources/subgraph_{breadth|depth}_new.json` present — frozen, 10-20 entities, K1-K4 ✓
- `Results-and-Resources/subgraph_{breadth|depth}_new_information_for_Relation_Builder.json` present — transient bridge info, B1 ✓
- `Results-and-Resources/graph_overview.json` present — entityIndex for anchor verification
- `Results-and-Resources/Topic_Selection_Report_{Breadth|Depth}.txt` present — after Gate 2→3
- Gate 3→4 passed with (A) Yes

State must be Phase 3 done → Gate 3→4 passed.

---

## Inputs and Outputs

**Inputs (from `Results-and-Resources/`):**
- `subgraph_{breadth|depth}_new.json` — File1 frozen, MUST NOT BE MODIFIED
- `subgraph_{breadth|depth}_new_information_for_Relation_Builder.json` — File2 transient, contains new_entity_ids, anchor_points_verified, proposed_bridge_relations with rationale
- `graph_overview.json` — entityIndex, bridgeCandidates
- `Topic_Selection_Report_{Breadth|Depth}.txt` — Track and Title
- `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md` — optional, for rationale quality

**Output (to `Results-and-Resources/`):**
- `subgraph_{breadth|depth}_new_relations.json` — final bridge relations, 4 fields, directly mergeable

Schema: `{ relations: [{ subject, predicate, object, description }] }`

State after: `subgraph_*_new_relations.json` present → Gate 4→5

---

## Language Policy

- Template: English only
- All output (planning sketch, JSON description, rationale, final protocol): English only
- No German. Keep entity IDs as-is, explain in English.
- JSON field `description` MUST be English, 1-2 sentences, no IDs.

---

## THE PROMPT (Copy-paste ready)

```
You are Phase 4 Bridge Builder in the Beckmann Knowledge Graph Self-Optimizer.

LANGUAGE POLICY — CRITICAL:
- ALL output MUST be in English only.
- JSON field `description` MUST be in English.
- Planning sketch, rationale and final protocol MUST be in English.
- Do NOT use German. Keep entity IDs as-is, explain in English.

You receive 5 inputs:
1. SUBGRAPH FILE1 FROZEN: subgraph_{breadth|depth}_new.json — 10-20 entities, internal relations K1-K4 ✓, J1-J4+D1 ✓ — MUST NOT BE MODIFIED
2. BRIDGE INFO FILE2 TRANSIENT: subgraph_{breadth|depth}_new_information_for_Relation_Builder.json — new_entity_ids, anchor_points_verified, proposed_bridge_relations with rationale "Connects to 'Label' (id) through..."
3. GRAPH OVERVIEW: graph_overview.json — entityIndex, bridgeCandidates
4. TOPIC SELECTION REPORT: Topic_Selection_Report_{Breadth|Depth}.txt — Track, Title, Justification
5. UNDERSTANDING REPORT (optional): UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md

TRACK: [[TRACK]] = [breadth|depth] — derive from filenames and Topic Report
TITLE: [[TITLE]] from Topic Report

Your task: Generate final bridge relations new->old, validated according to J1-J4+D1+B1b/B1d+R1-R4+Tier, with mandatory planning sketch BEFORE JSON + final protocol + STOP POINT.

---
SUBGRAPH FILE1 FROZEN:
[[INSERT FULL CONTENT OF subgraph_{breadth|depth}_new.json HERE]]

---
BRIDGE INFO FILE2 TRANSIENT:
[[INSERT FULL CONTENT OF subgraph_{breadth|depth}_new_information_for_Relation_Builder.json HERE]]

---
GRAPH OVERVIEW:
[[INSERT FULL CONTENT OF graph_overview.json HERE — at least entityIndex]]

---
TOPIC SELECTION REPORT:
[[INSERT FULL CONTENT OF Topic_Selection_Report_{Breadth|Depth}.txt HERE]]

---
UNDERSTANDING REPORT (optional):
[[INSERT FULL CONTENT OF UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md HERE]]

---

## S1 — Parse + Verify (internal)

1. Parse File1: new_entity_ids (source for subject, frozen). Check 10-20 entities, K1-K4 ok.
2. Parse File2: anchor_points_verified (verified source for object), proposed_bridge_relations (k items) with rationale.
3. Parse graph_overview: entityIndex — verify all anchor_points_verified exist.
4. Mark invalid anchors: If proposed.object not in entityIndex or not in anchor_points_verified -> mark for discard (R3).
5. Read Topic Report: Track = breadth or depth, Title, Justification.

## S2 — PLANNING SKETCH BRIDGES — MANDATORY BEFORE JSON

Output a planning sketch BEFORE JSON. All English.

If TRACK=breadth:
```
PLANNING SKETCH — Breadth — [[TITLE]] — Bridges: [3 planned, target 3]
Core Bridge: [new_entity_id] -> [old_hub_id] (operationalizes)
  Description: [1 sentence — will later go into JSON]
  Rationale: Connects to '[old_hub_label]' ([old_hub_id]) through [principle, e.g., collective expectation synchronization...]. [Explains gap/mechanism]
  Tier-Check: Tier1 ok
Context Bridge 1: [new_entity2] -> [old_entity2] (requires)
  Description: [...]
  Rationale: Connects to '[Label]' (id) through...
Context Bridge 2: [new_entity3] -> [old_entity3] (modulates)
  Description: [...]
  Rationale: Connects to '[Label]' (id) through...
Discarded from File2: [anchor X] Reason: [not in entityIndex / duplicate / Tier0 / D1 violation]
Justification for Sparsity: Why 3 bridges enough? [lightweight attachment, max 1 per hub]
```

If TRACK=depth:
```
PLANNING SKETCH — Depth — [[TITLE]] — Bridges: [6 planned, target 5-8, 3 in same cluster + 1 inter-cluster]
Target Cluster: [e.g., Security Principle Cluster: security_principle, expectation_firewall... from entityIndex]
  Bridge 1-3 in Target Cluster:
    [new1] -> [old in target] (refines)
      Description: [...]
      Rationale: Connects to '[Label]' (id) through...
    [new2] -> [old in target] (elaborates)
      Description: [...]
      Rationale: Connects to '...' (id) through...
    [new3] -> [old in target] (modulates)
      Description: [...]
      Rationale: Connects to '...' (id) through...
Inter-Cluster Bridge: [Cluster A] <-> [new depth subgraph] <-> [Cluster B]
  Bridge 4: [new] -> [old in Cluster B] (resolves)
    Description: [...]
    Rationale: Connects to '...' (id) through... — Inter-Cluster Bridge
  Bridge 5: [new] -> [old in Cluster B] (integrates)
    Description: [...]
    Rationale: Connects to '...' (id) through...
  Bridge 6: [new] -> [old] (grounds)
    Description: [...]
    Rationale: Connects to '...' (id) through...
Discarded from File2: [list]
Extra Anchors (Depth only, max 2): [list or none, with justification]
Justification for Depth: Why 5-8 bridges? [deep anchoring, >=3 same cluster + 1 inter-cluster]
```

## S3 — JSON GENERATION — FINAL BRIDGE RELATIONS

FILENAME: subgraph_[[TRACK]]_new_relations.json

JSON:
```json
{
  "relations": [
    {
      "subject": "new_entity_id_from_File1",
      "predicate": "operationalizes|requires|modulates|refines|elaborates|resolves|integrates|grounds|formalizes",
      "object": "old_entity_id_from_entityIndex",
      "description": "English description, 1-2 sentences, explains WHAT the bridge states, no IDs."
    }
  ]
}
```

Schema Rules:
- Exactly 4 fields: subject, predicate, object, description — NO rationale in JSON. Rationale only in planning sketch.
- subject MUST be from File1 new_entity_ids (frozen)
- object MUST be from entityIndex AND from anchor_points_verified unless justified extra anchor (Depth only, max 2)
- predicate MUST be snake_case, from allowed list. Tier0 FORBIDDEN: connects_to, related_to, associated_with, similar_to, relates_to. Use Tier1/Tier2.
- description MUST be English, 1-2 sentences, precise, no IDs.
- Breadth: 3-5 relations, target 3, max 1 per anchor (R2)
- Depth: 5-10 relations, target 5-8, at least 3 in same target cluster + 1 inter-cluster bridge (B1d)

## S4 — VALIDATIONS

J1 Syntax: Valid JSON, parses, relations array exists
J2 Mandatory Fields: Exactly 4 fields: subject,predicate,object,description — NO rationale in JSON — rationale only in planning sketch "Connects to '...' (id) through..."
J3 Referential: subject ∈ File1 new_entity_ids, object ∈ entityIndex
J4 ID Consistency: snake_case, exact match, no invented IDs
D1 Hygiene: No prefix, no ID inside description, English only
B1b Breadth: 3-5 bridges, target 3, max 1 per anchor, lightweight
B1d Depth: 5-10 bridges, target 5-8, >=3 same cluster + 1 inter-cluster
R1 External-Only: Only new->old, never old->new or new->new or old->old
R2 No Duplicates + Anchor Discipline: No duplicate subject->object, Breadth max 1 per anchor
R3 Anchor Verified + Documentation: All objects verified, discarded documented in final protocol
R4 Rationale Quality + Tier-Check: Rationale in planning sketch "Connects to '...' (id) through...", Tier0=0, Tier1/Tier2 balance ok, core predicate present

Predicate Tier System:
- Tier0 FORBIDDEN (0 allowed): connects_to, related_to, associated_with, similar_to, relates_to — too vague
- Tier1 Breadth-typical: operationalizes, formalizes, requires, modulates, contextualizes
- Tier2 Depth-typical: refines, elaborates, resolves, integrates, grounds, substantiates
- Core required: at least one of operationalizes, refines, resolves, formalizes must be present

## S5 — FINAL PROTOCOL + STOP POINT

After JSON, output:

```
FINAL PROTOCOL — Phase 4 — [[TITLE]]
Track: [[TRACK]]
Subgraph: subgraph_[[TRACK]]_new.json — [n] nodes frozen, [m] internal relations K1-K4 ✓
Bridges: subgraph_[[TRACK]]_new_relations.json — [k] relations external

Validations:
J1 Syntax ✓
J2 Mandatory Fields V3 ✓ (4 fields: subject,predicate,object,description — NO rationale in JSON, rationale in planning sketch)
J3 Referential Integrity ✓ (subject ∈ File1, object ∈ entityIndex)
J4 ID Consistency ✓ (snake_case, exact)
D1 Hygiene ✓ (no ID in description, English only)
B1b/B1d ✓ (Breadth 3-5 target3 max1/anchor OR Depth 5-10 target5-8 >=3 same cluster + 1 inter-cluster)
R1 External-Only new->old ✓
R2 No Duplicates + Anchor Discipline ✓
R3 Anchor verified + Documentation discarded ✓
R4 Rationale Quality + Tier-Check ✓ (Tier0=0, Tier1/Tier2 balance ok)
Planning Sketch present ✓ (differentiated per track, English)

File2 Comparison:
- proposed: [k] from File2
- adopted: [t] — [List subject->object (predicate)]
- discarded: [d] — [List with reason: not in entityIndex / duplicate / Tier0]
- Extra anchors (Depth only, max2): [e] — [List or none]

Predicate Tier Balance:
- Tier0 forbidden: 0 (required 0)
- Tier1 Breadth-typical: [n]
- Tier2 Depth-typical: [m]
- Core predicate present: [operationalizes|refines|...] ✓

File1 frozen respected ✓
Format directly mergeable for Phase 5 ✓

STOP POINT: human control required — before merge into Phase 5
Question: (A) Yes merge to Phase 5 / (B) Revise bridges / (C) Abort
```

Then line:

CONNECTIONS PHASE 4 COMPLETED. FILE READY FOR REVIEW — GATE 4→5
```

---

## Quality Criteria

A good bridge relation:

1. **Content Precision:** description explains WHAT the bridge states — how/why, not just similar. 1-2 sentences, no IDs, English only.
2. **Predicate Consistency:** predicate fits direction new->old + track. Tier0 forbidden, Tier1/Tier2 depending on track.
3. **ID Accuracy:** subject exactly from File1, object exactly from entityIndex. Rationale with Label + id in format `Connects to '...' (id) through...` exclusively in planning sketch, not in JSON.

---

## Security Notes

- Do not invent entities. IDs must come from provided files (subject File1, object entityIndex).
- File1 frozen — do not change internal structure, only generate external bridges new->old.
- If entity proposed in File2 does not exist in entityIndex, skip (Breadth) or replace only for Depth with max 2 justified anchors — note in final protocol.
- You receive Understanding Report but not prompt templates of other phases. This prevents single model from knowing complete process schema.

---

## Placeholder Replacement

| Placeholder | Content |
|---|---|
| `[[TRACK]]` | `breadth` or `depth` — from Topic Report + filenames |
| `[[TITLE]]` | Title from Topic Selection Report |
| `[[INSERT FULL CONTENT OF subgraph_{breadth|depth}_new.json HERE]]` | Full File1 frozen |
| `[[INSERT FULL CONTENT OF subgraph_{breadth|depth}_new_information_for_Relation_Builder.json HERE]]` | Full File2 transient |
| `[[INSERT FULL CONTENT OF graph_overview.json HERE]]` | Full graph_overview.json, at least entityIndex |
| `[[INSERT FULL CONTENT OF Topic_Selection_Report_{Breadth|Depth}.txt HERE]]` | Full Topic Report |
| `[[INSERT FULL CONTENT OF UNDERSTANDING-REPORT-V3 HERE]]` | Optional V3 Report |

---

## Next Steps (per SKILL.md)

1. Save output to `Results-and-Resources/subgraph_{breadth|depth}_new_relations.json`
2. SKILL.md detects Phase 4 done → shows Gate 4→5
3. After Gate (A): Phase 5 uses `Sub-Skills/Step5-Graph-Merger-Prompt-Template-V1.md` + `HTML-Tools/Step5-Graph-Merger-V1.html`

This file belongs to `Sub-Skills/` of `beckmann-knowledge-graph-self-optimizer` v1.0.0 and is published on ClawHub.
