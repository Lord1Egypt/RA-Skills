---
name: disease-drug-intelligence
description: A disease-to-innovative-drug analysis skill for biomedical question answering. It is used to answer questions such as "What innovative, cutting-edge, pipeline, or novel-mechanism drugs exist for a given disease?" and produces an integrated evidence report covering disease, targets, drugs, clinical progress, and mechanism trends. It is designed for multi-database querying, normalization, innovation filtering, and structured report generation using local adapters for ChEMBL, ClinicalTrials, and Search.
license: Proprietary
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - python3
      env:
        - TAVILY_API_KEY
      config: []
    always: false
    emoji: "💉"
    homepage: https://github.com/ClawBio/ClawBio
    os: [darwin, linux]
    install:
      - kind: pip
        package: requests
        bins: []
      - kind: pip
        package: langchain-tavily
        bins: []
    trigger_keywords:
      - innovative drugs
      - pipeline drugs
      - disease drug landscape
      - clinical competition landscape
      - drug pipeline
      - clinical trials
      - chembl
---

# Disease Innovative Drug Intelligence Integration

## Overview

Convert natural-language questions such as "What noteworthy new drugs have recently emerged for Alzheimer's disease?" into executable multi-database query plans.
Generate a decision-oriented English comprehensive report rather than a simple list of drug names.

## Quick Start

1. Identify whether the request belongs to the `disease_to_drug` scenario.
2. Standardize the disease entity and decompose the "innovative drug" intent.
3. Prefer the local `local_tools/` code for database queries.
4. Perform entity normalization, evidence integration, innovation filtering, and tiered output.
5. Generate the final report and annotate evidence boundaries.

For detailed data structures, routing rules, scoring logic, and the report template, see [disease_to_drug_playbook.md](references/disease_to_drug_playbook.md).

## Local Execution Rules

This skill no longer depends on a BioDB MCP HTTP service.
For any `ChEMBL`, `ClinicalTrials`, or `Search` call, only use the local Python code bundled in the current skill directory:

- `local_tools/chembl_api.py`
- `local_tools/clinicaltrials_api.py`
- `local_tools/search_api.py`
- `local_tools/run_tool.sh`

Recommended commands:

```bash
bash local_tools/run_tool.sh chembl_api.py search_target EGFR
bash local_tools/run_tool.sh chembl_api.py search_molecule osimertinib
bash local_tools/run_tool.sh chembl_api.py get_drug_by_id CHEMBL3545063
bash local_tools/run_tool.sh clinicaltrials_api.py get_studies --query-cond "lung cancer" --fields NCTId BriefTitle OverallStatus
bash local_tools/run_tool.sh search_api.py "latest EGFR inhibitor approval"
```

Execution constraints:

- Prefer importing local `local_tools/` modules or executing them through `bash local_tools/run_tool.sh ...`. Do not assume services such as `http://127.0.0.1:8086` exist.
- Do not depend on bare `python` commands directly. Always use `run_tool.sh` to resolve the available interpreter. `run_tool.sh` prefers `python3` and only falls back to `python` if needed.
- If `Search` is needed, confirm that `langchain_tavily` is installed and the `TAVILY_API_KEY` environment variable is set.
- The current database capability set only includes `ChEMBL`, `ClinicalTrials`, and `Search`. Ignore any other database descriptions that are not implemented in this skill.
- `Search` may only be executed via `bash local_tools/run_tool.sh search_api.py ...` or `SearchAPI.run(query)`. Do not bypass the local tool and call an external web search directly.
- Only when the user explicitly asks for external web search and also states that the local `Search` tool is unavailable or insufficient may external web search be used as a final fallback. Otherwise it is forbidden.

## Trigger and Detection

Trigger this skill when the user question contains both of the following:
- A disease entity, such as diabetes, lung cancer, Alzheimer's disease, obesity, NASH, or RA.
- An innovative-drug intent, such as innovative drugs, novel-mechanism drugs, pipeline drugs, cutting-edge drugs, or noteworthy new drugs.

If the request is overly broad, such as "innovative drugs for cancer," first suggest narrowing the disease type. If the user does not want to narrow it, default to a top cancer types plus top mechanisms overview.

## Workflow

### Step 0 Task Structuring

Construct a task object such as:

```json
{
  "task_type": "disease_to_drug",
  "focus": "innovative_drugs",
  "disease_raw": "diabetes",
  "time_constraint": null,
  "region_constraint": null,
  "stage_constraint": null
}
```

### Step 1 Disease Normalization

Output `canonical_disease`, `subtypes`, `aliases`, and `preferred_query_terms`.
If the user does not specify a subtype, first analyze the overall disease, then emphasize more active R&D subtypes, for example prioritizing T2DM under diabetes.

### Step 2 Innovative Drug Mapping

Map "innovative drugs" into executable criteria:
- New mechanisms or new targets, including first-in-class tendency
- Representative recently approved drugs
- Mid-to-late stage pipeline candidates, with Phase II/III preferred
- Frontier directions such as dual or multi-target drugs and next-generation optimized molecules

### Step 3 Subtask Decomposition

Always execute these five subtasks:
- `identify_targets_and_mechanisms`
- `retrieve_representative_drugs`
- `build_drug_profiles`
- `validate_clinical_progress`
- `summarize_trends`

### Step 4 Database Execution Order

Default order:
1. Mechanisms and targets: `ChEMBL(target/mechanism)`
2. Drug candidates: `ChEMBL(molecule/drug/indication)`
3. Clinical progress: `ClinicalTrials`
4. Web fallback: `Search`, only through local `search_api.py`, and only when `ChEMBL` and `ClinicalTrials` evidence is insufficient or recent updates need verification

Notes:
- This skill no longer depends on a BioDB MCP service.
- `ChEMBL`, `ClinicalTrials`, and `Search` have been switched to local adapter code.
- The stable execution scope of this skill only covers these three capabilities.

### Step 5 Evidence Integration and Deduplication

Primary keys in priority order:
- Drug: `ChEMBL ID > standard drug name > ClinicalTrials intervention`
- Target: `gene symbol or standard target name > alias`

Always preserve aliases and dosage-form information to avoid incorrect merges, such as different semaglutide formulations.

### Step 6 Innovation Filtering and Ranking

Score from 0 to 5 and rank comprehensively across:
- `disease_relevance`
- `innovation`
- `clinical_maturity`
- `evidence_strength`
- `representativeness`

Output must be tiered into:
- Approved or clinically validated representative innovative drugs
- Mid-to-late stage pipeline candidates
- Frontier exploratory mechanism directions

### Step 7 Report Generation

Before generating the report, first read `## 10. English Report Template` in `references/disease_to_drug_playbook.md`.

By default, the final report must strictly follow that template. Do not produce a free-form answer that merely "covers the same topics." The section order, first-level numbering, and main title skeleton must remain unchanged:

- `{Disease Name} Innovative Drug Analysis Report`
- `1. Problem Overview`
- `2. Executive Summary`
- `3. Key Disease-Related Targets and Mechanisms`
- `4. Representative Innovative Drug List`
- `5. Clinical Trial Progress Overview`
- `6. R&D Trends and Assessment`
- `7. Result Notes and Limitations`

Only if the user explicitly asks for a brief version, summary version, table version, or another specific format may you deviate from the standard template. Otherwise you must use it.

### Step 8 Exception Handling

- Too many results: use representativeness plus innovation to select Top N, default `10`.
- Too few results: prioritize target directions and adjacent mechanisms rather than forcing a drug list.
- Conflicting evidence: clearly state that molecular evidence exists while clinical evidence is limited.
- Missing constraints: default to `time_constraint=null` and `region_constraint=global`, then state this explicitly in the report.

## Tool-Usage Constraints

- Run the main path first, meaning local `ChEMBL` plus local `ClinicalTrials`, and only then supplement. Do not reverse the order.
- If key fields such as phase, status, or target are missing, a supplementary query must be triggered.
- Every key conclusion in the report must have at least one traceable evidence item with database name plus entity primary key.
- Do not treat "innovative drugs" as a regulatory term. It is an information-integration term and must be declared as such in the result notes.
- For the minimum required `ChEMBL` capability set, prefer `search_target`, `search_molecule`, `get_drug_by_id`, `get_molecule_by_id`, `get_target_by_id`, `get_mechanism`, and `get_drug_indication`.
- For the minimum required `ClinicalTrials` capability set, prefer `get_studies` and `get_study`.
- For the minimum required `Search` capability set, always use `SearchAPI.run(query)`. If dependencies or API keys are missing, state in the result that supplementary retrieval could not be executed, and do not automatically switch to external web search.
- When executing local tools from the command line, always use `bash local_tools/run_tool.sh <tool.py> ...`. Do not write `python <tool.py> ...` directly.
- Do not reintroduce `KEGG`, `UniProt`, `STRING`, `Ensembl`, `PubChem`, `PDB`, or any other database instructions not included in the current code layer.
- Before output, self-check whether the report sections match `## 10. English Report Template` exactly. If they do not, rewrite before sending.

## Quality Checklist

- Was disease normalization completed, including aliases and subtypes?
- Does the report provide a mechanism-drug-clinical three-layer evidence chain?
- Were entity normalization and alias deduplication completed?
- Is the output tiered into approved, mid-to-late stage, and frontier directions?
- Are limitations, conflicts, and uncertainty clearly stated?

## Reference File

- [disease_to_drug_playbook.md](references/disease_to_drug_playbook.md): Full SOP, routing strategy, internal JSON structures, and the English report template.
