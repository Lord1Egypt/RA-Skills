# beckmann-knowledge-graph-self-optimizer

> Iterative self-optimization of a knowledge graph (`graph.json`) in 5 phases with 3 mandatory review gates and a final merge + cleanup cycle.

**Version:** 1.1.0 | **Language:** English | **Target:** ClawHub  
**License:** MIT | **Author:** Beckmann

---

## What is this?

One skill for ClawHub that orchestrates the complete optimization cycle of a large knowledge graph:

* Works with any generic knowledge graph (`entities` / `relations` or `nodes` / `edges`)
* No hardcoded Beckmann logic in the core — Beckmann checks are optional domain hints
* Offline HTML tools, no data upload
* Pause/resume at any phase, state detection via `Results-and-Resources/`


---

## Folder Structure

```
beckmann-knowledge-graph-self-optimizer/
├── SKILL.md                  ← global orchestrator (this skill)
├── README.md
├── package.json
├── CHANGELOG.md
├── Sub-Skills/
│   ├── Step1-Understanding-Prompt-Template-V3.md
│   ├── Step2-Breadth-Topic-Suggester-Prompt-Template-V1.md
│   ├── Step2-Depth-Topic-Suggester-Prompt-Template-V1.md
│   ├── Step3-Subgraph-Builder-Prompt-Template-V1.md
│   ├── Step4-Relation-Builder-Prompt-Template-V3.md
│   └── Step5-Graph-Merger-Prompt-Template-V1.md
├── HTML-Tools/
│   ├── Graph-Overview-Generator.html
│   ├── Knowledge-Graph-Splitter.html
│   └── Step5-Graph-Merger-V1.html
└── Results-and-Resources/    ← STATUS FOLDER — skill reads this on every start
    └── graph.json (placed by user)
```

---

## Requirements

* Modern browser (Chrome/Edge/Firefox) for `HTML-Tools/` — offline, no upload
* `graph.json` valid JSON, tested with 2k-15k nodes
* AI model with large context for Sub-Skills (Claude, GPT-4o, Meta AI etc.)

---

## Quickstart

1. Place `graph.json` into `Results-and-Resources/`
2. Activate skill `beckmann-knowledge-graph-self-optimizer`
3. Follow phases:

   * Phase 1a: `Graph-Overview-Generator.html` → `graph\_overview.json`
   * Phase 1b: `Knowledge-Graph-Splitter.html` → `graph\_Part\_1\_of\_4.json` … `Part\_4\_of\_4.json`
   * Phase 1c: Sub-Skill Step1 → `UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md`
   * Phase 2: Sub-Skill Step2 Breadth OR Depth → `Topic\_Selection\_Report\_\*.txt`
   * Gate 2→3: (A) Yes
   * Phase 3: Sub-Skill Step3 → `subgraph\_\*\_new.json` + `\*\_information\_for\_Relation\_Builder.json`
   * Gate 3→4: (A) Yes
   * Phase 4: Sub-Skill Step4 → `subgraph\_\*\_new\_relations.json`
   * Gate 4→5: (A) Yes
   * Phase 5a: Sub-Skill Step5 briefing
   * Phase 5b: `Step5-Graph-Merger-V1.html` → `graph\_vNEXT\_optimized.json`
4. Post-Merge Protocol: Backup → Rename `graph\_vNEXT\_optimized.json` → `graph.json` → Verify → Cleanup

You can pause after any phase or gate and reactivate later — the skill detects state from files present.

---

## Workflow Overview

```
START: Results-and-Resources/ empty
  → User places graph.json
  ↓
Phase 1a: Overview → graph\_overview.json
Phase 1b: Split → 4 parts
Phase 1c: Understanding → UNDERSTANDING-REPORT
  ↓
Phase 2: Topic Selection → Topic\_Selection\_Report\_\*.txt
  ↓
Gate 2→3: MANDATORY STOP
  ↓ (A)
Phase 3: Subgraph Builder (10-20 entities frozen) + bridge info
  ↓
Gate 3→4: MANDATORY STOP
  ↓ (A)
Phase 4: Relation Builder (3-5 Breadth / 5-10 Depth bridge relations)
  ↓
Gate 4→5: MANDATORY STOP
  ↓ (A)
Phase 5a: Graph Merger briefing
Phase 5b: Merger HTML → graph\_vNEXT\_optimized.json
  ↓
Post-Merge: Backup → Rename → Verify → Cleanup → new graph.json
  ↓
Next cycle
```

---

## Operating Policies

**HTML Tools — User-Operated Only:**
Client-side, offline, no external data transfer. Agent only instructs and waits for file presence. Never executed programmatically by agent.

> Note: The HTML tools process your graph data locally in the browser. Entity IDs, descriptions, hub lists, and other graph content will be copied into the generated output files (e.g. `graph_overview.json`, split parts). Treat these output files as potentially sensitive if your graph contains confidential information. No data is sent to any server.

**Review Gates:**
Explicit (A) required to proceed. (B) revise, (C) abort. No implicit approval from "looks good".

**Safe Loading:**
Sub-Skill templates loaded by exact filename from `Sub-Skills/`. Missing template or input file → stop with exact missing file name.

---

## Sub-Skills in V1.1.0

|Phase|File|Output|
|-|-|-|
|1c|`Step1-Understanding-Prompt-Template-V3.md`|`UNDERSTANDING-REPORT-V3-From-Parts-And-Overview.md`|
|2 Breadth|`Step2-Breadth-Topic-Suggester-Prompt-Template-V1.md`|`Topic\_Selection\_Report\_Breadth.txt`|
|2 Depth|`Step2-Depth-Topic-Suggester-Prompt-Template-V1.md`|`Topic\_Selection\_Report\_Depth.txt`|
|3|`Step3-Subgraph-Builder-Prompt-Template-V1.md`|`subgraph\_\*\_new.json` + `\*\_information\_for\_Relation\_Builder.json`|
|4|`Step4-Relation-Builder-Prompt-Template-V3.md`|`subgraph\_\*\_new\_relations.json` (4 fields, EN, rationale-free)|
|5a|`Step5-Graph-Merger-Prompt-Template-V1.md`|briefing for merger|
|5b|`Step5-Graph-Merger-V1.html`|`graph\_vNEXT\_optimized.json`|

All templates V1.1.0 cleaned: English only, no legacy version hints, `Results-and-Resources/` with hyphen, no prefix logic.

---

## Language Policy

* All prompt templates: English only
* All gate review blocks: English
* All relation content (`predicate`, `description`): English only
* This README: English (ClawHub publication)

---

## Installation for ClawHub

1. Install skill `beckmann-knowledge-graph-self-optimizer` from ClawHub
2. Ensure `Results-and-Resources/` exists
3. Place your `graph.json` inside
4. Activate skill

No `npm install` needed — HTML tools run offline in browser.

---
