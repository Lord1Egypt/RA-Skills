---
name: step5-graph-merger
version: 1.0.0
phase: 5
skill: beckmann-knowledge-graph-self-optimizer
description: Guide for final graph assembly via HTML merger tool — generates graph_vNEXT_optimized.json
author: Beckmann
license: MIT
tags: [knowledge-graph, graph-merger, assembly, ClawHub]
language: English
target: ClawHub
---

# Prompt Template — Step 5: Graph Merger (Assembly)

**Skill:** `beckmann-knowledge-graph-self-optimizer` v1.0.0  
**Template:** `Step5-Graph-Merger-Prompt-Template-V1.md`  
**Phase:** 5 — Graph Assembly (Final Merge)

---

## Purpose

This sub-skill tells the global orchestrator skill what to do when Gate 4→5 has passed with (A) Yes.

Phase 5 does not generate reports or overviews. It has one job: guide the human user to assemble the new graph using the HTML merger tool and produce `graph_vNEXT_optimized.json`.

---

## Trigger Condition

Use this template only when:

```
Gate 4→5 Review = (A) Yes — Merge final
- Subgraph frozen: subgraph_{breadth|depth}_new.json exists (10-20 nodes, K1-K4 ✓)
- Relations frozen: subgraph_{breadth|depth}_new_relations.json exists (4 fields, EN, rationale-free, directly mergeable)
- Validations J1-J4, D1, B1b/B1d, R1-R4, Tier, English-Only all ✓
```

No other files required for Phase 5 start.

---

## Inputs and Outputs

**Inputs (from `Results-and-Resources/`, 3 files only):**
1. `graph.json` — base graph
2. `subgraph_breadth_new.json` OR `subgraph_depth_new.json` — frozen from Phase 3
3. `subgraph_breadth_new_relations.json` OR `subgraph_depth_new_relations.json` — frozen from Phase 4, 4 fields, English, rationale-free

**Tool:**
- `HTML-Tools/Step5-Graph-Merger-V1.html` — client-side, offline, user-operated

**Output (to `Results-and-Resources/`):**
- `graph_vNEXT_optimized.json` — single output, auto-downloaded

Then manual user action:
- Backup → Rename `graph_vNEXT_optimized.json` → `graph.json` → Verify → Cleanup

State after: `graph_vNEXT_optimized.json` present → Post-Merge Protocol

---

## Language Policy

- Template: English only
- All user-facing text: English only
- Tool UI: English only

---

## THE PROMPT — What the Global Skill Must Output (English Only)

When Phase 5 starts, the global skill must not run code. It must output only the following English text block verbatim to the human user.

```
=== PHASE 5 — GRAPH ASSEMBLY — READY FOR MERGE ===

Gate 4→5 has passed. All validations from Phase 3 and Phase 4 are complete.

Your 3 input files for final merge are:
1. graph.json (base graph)
2. subgraph_breadth_new.json OR subgraph_depth_new.json (frozen from Phase 3)
3. subgraph_breadth_new_relations.json OR subgraph_depth_new_relations.json (frozen from Phase 4 — 4 fields, English, rationale-free)

Tool to use:
HTML-Tools/Step5-Graph-Merger-V1.html

This tool is client-side, offline, user-operated. No data is sent externally.

--- HOW TO USE THE TOOL ---

1. Open HTML-Tools/Step5-Graph-Merger-V1.html in your browser.

2. Step 1 — Base Graph:
   Click [Load base graph]. The tool accepts ONLY file name 'graph.json'.
   If you select a wrong file, it will be rejected with an error message.
   On success, button becomes disabled and shows green check: ✔ graph.json loaded.

3. Step 2 — New Subgraph:
   Click [Load new subgraph]. The tool accepts ONLY 'subgraph_breadth_new.json' OR 'subgraph_depth_new.json'.
   On success, button disabled + green check.

4. Step 3 — New Relations:
   Click [Load new relations]. The tool accepts ONLY 'subgraph_breadth_new_relations.json' OR 'subgraph_depth_new_relations.json'.
   On success, button disabled + green check.

5. Step 4 — Generate:
   [Generate Merged Graph] is disabled until all 3 files show green checks.
   When active, click it. The tool merges via deduplication (seenIds + relSet) and shows statistics:
   Total Nodes, Total Relations, Duplicate Nodes Skipped, Duplicate Relations Skipped, plus merge log.
   File graph_vNEXT_optimized.json will be auto-downloaded. You can re-download via [Download graph_vNEXT_optimized.json].

6. After merge, a banner appears:
   Success! File 'graph_vNEXT_optimized.json' has been generated.
   NEXT STEP: Rename to 'graph.json' for next cycle.

--- RENAME FOR NEXT CYCLE (USER ACTION) ---

Rename the generated file:

graph_vNEXT_optimized.json -> graph.json

Commands:
  Windows:   ren graph.json old_graph.json
             ren graph_vNEXT_optimized.json graph.json
  Mac/Linux: mv graph.json old_graph.json
             mv graph_vNEXT_optimized.json graph.json

This renamed file is your new base graph for next cycle.

--- VERIFY ---

Open new graph.json and confirm:
- File opens without errors
- New entities from this cycle are present

--- CLEANUP — DELETE OLD FILES (USER ACTION AFTER VERIFICATION) ---

Delete from Results-and-Resources/ after successful verification:

- old_graph.json (previous version — only AFTER verifying new one)
- graph_Part_1_of_4.json
- graph_Part_2_of_4.json
- graph_Part_3_of_4.json
- graph_Part_4_of_4.json
- graph_overview.json
- UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md
- Topic_Selection_Report_Breadth.txt / Topic_Selection_Report_Depth.txt
- subgraph_breadth_new.json / subgraph_depth_new.json
- subgraph_breadth_new_information_for_Relation_Builder.json / subgraph_depth_new_information_for_Relation_Builder.json
- subgraph_breadth_new_relations.json / subgraph_depth_new_relations.json

Keep in Results-and-Resources/:
- new graph.json (renamed from graph_vNEXT_optimized.json) ✓

Keep everywhere else:
- All HTML-Tools/ files
- All Sub-Skills/ templates
- SKILL.md, README.md, CHANGELOG.md, package.json

Phase 5 is complete when graph_vNEXT_optimized.json has been generated. No other output file is expected from Phase 5.
```

---

## Rules for Global Skill

- **Language:** Output MUST be 100% English
- **No extra file generation:** Do not generate release_notes.md, graph_overview.json or any report in Phase 5
- **Tool naming:** Always refer to tool as `HTML-Tools/Step5-Graph-Merger-V1.html`
- **Foolproof:** Explicitly mention that wrong filenames are rejected with error message
- **Rename:** Always include exact rename instruction `graph_vNEXT_optimized.json` → `graph.json` and backup to `old_graph.json`
- **Cleanup:** Always include full delete list
- **Wait for confirmation:** After showing text block, stop and wait for user confirmation that merge + save is complete

---

## Next Steps (per SKILL.md)

1. User runs `HTML-Tools/Step5-Graph-Merger-V1.html` and saves `graph_vNEXT_optimized.json` to `Results-and-Resources/`
2. SKILL.md detects `graph_vNEXT_optimized.json` present → Post-Merge Protocol
3. Post-Merge: User Backup → Rename → Verify → Cleanup → new `graph.json` ready for next cycle

This file belongs to `Sub-Skills/` of `beckmann-knowledge-graph-self-optimizer` v1.0.0 and is published on ClawHub.
