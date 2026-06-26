# disease-drug-intelligence

`disease-drug-intelligence` is a publishable Claw-style skill for generating Chinese disease-to-drug intelligence reports. It combines local Python adapters for ChEMBL, ClinicalTrials.gov, and Tavily Search with a structured `SKILL.md` methodology so an agent can turn natural-language questions into reproducible evidence-backed outputs.

## What This Skill Does

- Standardizes disease entities and innovation intent from user questions.
- Queries ChEMBL for targets, molecules, mechanisms, and indications.
- Queries ClinicalTrials.gov for study-level evidence and trial progress.
- Uses Tavily search only as a controlled fallback for recent public updates.
- Produces a structured Chinese report covering targets, representative drugs, clinical progress, trends, and limitations.

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── local_tools/
│   ├── __init__.py
│   ├── chembl_api.py
│   ├── clinicaltrials_api.py
│   ├── run_tool.sh
│   └── search_api.py
├── references/
│   └── disease_to_drug_playbook.md
├── requirements.txt
└── skill-manifest.json
```

## Why The Packaging Looks Like This

This project is a Python-based Claw/OpenClaw skill, not a Node.js MCP package. Because of that:

- `SKILL.md` is the primary artifact for agent routing and methodology.
- `requirements.txt` is the correct dependency file, rather than `package.json`.
- `skill-manifest.json` provides machine-readable tool metadata, including `name`, `description`, and `inputSchema`.
- A true `mcp-config.json` is not included because this repository does not yet implement an MCP server process. The current release shape is a local-first skill plus callable CLI tools.

## Tooling

### `chembl_api.py`

ChEMBL adapter with the following commands:

- `search_target`
- `search_molecule`
- `get_drug_by_id`
- `get_molecule_by_id`
- `get_target_by_id`
- `get_mechanism`
- `get_drug_indication`

### `clinicaltrials_api.py`

ClinicalTrials.gov adapter with the following commands:

- `get_studies`
- `get_study`

### `search_api.py`

Tavily-backed search adapter:

- `run`

## Installation

```bash
cd /home/xiaoxiao/projects/disease-drug-intelligence
python3 -m pip install -r requirements.txt
```

Optional environment variable for the search fallback:

```bash
export TAVILY_API_KEY="your_api_key"
```

## Example Commands

```bash
bash local_tools/run_tool.sh chembl_api.py search_target EGFR
bash local_tools/run_tool.sh chembl_api.py get_drug_by_id CHEMBL3545063
bash local_tools/run_tool.sh clinicaltrials_api.py get_studies --query-cond "lung cancer" --fields NCTId BriefTitle OverallStatus
bash local_tools/run_tool.sh search_api.py "latest EGFR inhibitor approval"
```

## Publish Readiness Notes

- `SKILL.md` now includes versioning, tags, and `metadata.openclaw` fields for discoverability.
- `agents/openai.yaml` provides UI-facing name and summary.
- `skill-manifest.json` gives marketplaces a machine-readable inventory of exposed tools.
- The repository remains compatible with Claw-style skill runners that read markdown instructions and invoke local scripts.
