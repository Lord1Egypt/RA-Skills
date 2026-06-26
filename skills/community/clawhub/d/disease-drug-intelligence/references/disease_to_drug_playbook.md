# Disease-to-Innovative-Drug Playbook

## 1. Task Object

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

## 2. Disease Normalization Output Structure

```json
{
  "canonical_disease": "diabetes mellitus",
  "subtypes": ["type 1 diabetes mellitus", "type 2 diabetes mellitus"],
  "aliases": ["diabetes", "DM", "T1DM", "T2DM"],
  "preferred_query_terms": ["diabetes mellitus", "type 2 diabetes", "type 1 diabetes"]
}
```

## 3. Internal Definition of Innovative Drugs

```json
{
  "innovation_definition": {
    "include_new_mechanism": true,
    "include_recent_approved": true,
    "include_late_stage_pipeline": true,
    "include_frontier_candidates": true
  }
}
```

## 4. Fixed Subtask Chain

```json
{
  "subtasks": [
    "identify_targets_and_mechanisms",
    "retrieve_representative_drugs",
    "build_drug_profiles",
    "validate_clinical_progress",
    "summarize_trends"
  ]
}
```

## 5. Database Routing Table

| Subtask | Goal | Primary Database | Supporting Database | Output Focus |
|---|---|---|---|---|
| Disease normalization | Standard name, aliases, subtypes | Internal rules | Search | Standardized disease entity |
| identify_targets_and_mechanisms | Find key targets and mechanism directions | ChEMBL | Search | Targets and mechanism directions |
| retrieve_representative_drugs | Retrieve representative drugs and candidates | ChEMBL | None | Drug entities, mechanisms, indications |
| build_drug_profiles | Build drug profiles | ChEMBL | None | Drug-target-mechanism structure |
| validate_clinical_progress | Verify clinical progress | ClinicalTrials | Search | Phase, status, NCT |
| summarize_trends | Summarize trends | ClinicalTrials, ChEMBL | Search | Hot directions and R&D landscape |

Notes:
- The stable execution scope of the current skill only covers `ChEMBL`, `ClinicalTrials`, and `Search`.
- `Search` is only used as a local fallback for disease alias enrichment, recent-update verification, and cases where database evidence is insufficient. Do not bypass the bundled `local_tools/search_api.py` or `local_tools/run_tool.sh` to call external web search directly.

## 6. Query Priority and Granularity

Priority:
1. Mechanism and target scaffold (`ChEMBL`)
2. Drug candidate pool (`ChEMBL`)
3. Clinical validation (`ClinicalTrials`)
4. Local search reinforcement (`Search`)

Granularity strategy:
- Broad questions such as "innovative drugs for diabetes": start with the full disease area, then focus on the most active subtype.
- Mechanism-constrained questions such as "GLP-1 innovative drugs": lock the mechanism first, then expand to drugs.
- Time-constrained questions such as "in the last five years": increase the weight of recent trials and recent approvals.
- Region-constrained questions such as "China": use `ClinicalTrials` plus `Search` to strengthen regional filtering.
- If the `Search` tool is unavailable, explicitly state that supplementary retrieval was not performed. Do not automatically switch to external web search.

## 7. Evidence Integration and Deduplication

Drug primary-key priority:
1. ChEMBL ID
2. Standard drug name
3. ClinicalTrials intervention name after normalization

Target primary-key priority:
1. Gene symbol or standard target name
2. Standard target name
3. Alias

Unified drug candidate pool structure:

```json
[
  {
    "drug_name": "...",
    "aliases": ["..."],
    "target": ["..."],
    "mechanism": "...",
    "evidence": {
      "chembl": {},
      "clinicaltrials": {},
      "search_support": {}
    }
  }
]
```

## 8. Innovation Scoring

```json
{
  "disease_relevance": 0,
  "innovation": 0,
  "clinical_maturity": 0,
  "evidence_strength": 0,
  "representativeness": 0
}
```

Output tiers:
- Approved or clinically validated representative innovative drugs
- Mid-to-late stage pipeline candidates
- Frontier exploratory mechanism directions

## 9. Exception Handling

- Disease scope too broad, such as "innovative drugs for cancer": first suggest narrowing the cancer type; otherwise output top cancer types plus top mechanisms.
- Evidence inconsistency across databases: explicitly state "mechanistic evidence exists, but clinical evidence is weak or not detected."
- Too many results: output Top N by default, recommended `10`.
- Too few results: switch to "target direction + adjacent mechanisms + trend assessment."
- `Search` unavailable: explicitly state "Local Search supplementary retrieval was not executed in this run." Do not automatically switch to external web search.

## 10. English Report Template

```markdown
{Disease Name} Innovative Drug Analysis Report

1. Problem Overview
- The user is interested in noteworthy innovative drugs in the {Disease Name} area.
- In this report, "innovative drugs" includes drugs with new mechanisms or new targets, representative recently approved drugs, mid-to-late stage pipeline candidates, and frontier exploratory directions.

2. Executive Summary
- The most important directions at present are: {Direction 1}, {Direction 2}, {Direction 3}
- Drug tiers:
  - Representative innovative drugs that are approved or have relatively strong clinical validation
  - Candidate drugs advancing through mid-to-late clinical development
  - Exploratory directions that are mechanistically frontier but still early stage

3. Key Disease-Related Targets and Mechanisms
3.1 Key Targets
- {Target 1}: {Brief functional description}
- {Target 2}: {Brief functional description}
- {Target 3}: {Brief functional description}

3.2 Mechanism Summary
- {Mechanism Direction 1}
- {Mechanism Direction 2}
- {Mechanism Direction 3}

4. Representative Innovative Drug List
4.1 Approved or Relatively Mature
- Drug: {drug_name}
- Main target/mechanism: {target/mechanism}
- Indication relevance: {indication}
- Innovation point: {why_innovative}
- Clinical or market status: {status}
- Notes: {remark}

4.2 Mid-to-Late Stage Pipeline Candidates
- Drug: {drug_name}
- Main target/mechanism: {target/mechanism}
- Current phase: {phase}
- Why it matters: {reason}
- Risk or uncertainty: {risk}

4.3 Frontier Exploratory Directions
- {Direction 1}: {Explanation}
- {Direction 2}: {Explanation}

5. Clinical Trial Progress Overview
5.1 Active Directions
- {Direction 1}
- {Direction 2}
- {Direction 3}

5.2 Trial Characteristics
- Common phases: {I/II/III}
- Common intervention types: {small_molecule/peptide/antibody/combination}
- Recruitment status overview: {recruiting/active/completed}

6. R&D Trends and Assessment
- Trends: {Trend 1}, {Trend 2}, {Trend 3}
- Relatively mature direction: {Direction A}
- Frontier exploratory direction: {Direction B}

7. Result Notes and Limitations
- This report is a multi-database evidence integration result.
- "Innovative drug" is an information-integration concept, not a strict regulatory definition.
- When clinical evidence is limited for early-stage candidates, combine local Search output and public-source cross-checking for further judgment.
```

## 11. Hard Execution Constraints

- Only use the local tools bundled with the current skill: `local_tools/chembl_api.py`, `local_tools/clinicaltrials_api.py`, and `local_tools/search_api.py`.
- For command-line execution, always call local tools through `bash local_tools/run_tool.sh <tool.py> ...`. Do not rely on bare `python` commands directly.
- Do not reintroduce `KEGG`, `UniProt`, `STRING`, `Ensembl`, `PubChem`, `PDB`, `OpenTargets`, or any database requirements not included in the current code layer.
- `Search` may only be executed through `SearchAPI.run(query)` or `bash local_tools/run_tool.sh search_api.py ...`.
- If `Search` dependencies or API key are missing, only state that the capability is unavailable in the result. Do not automatically switch to external web search.
- Before producing the final answer, verify line by line that the output strictly matches the main title, numbering, and section order defined in `## 10. English Report Template`.
