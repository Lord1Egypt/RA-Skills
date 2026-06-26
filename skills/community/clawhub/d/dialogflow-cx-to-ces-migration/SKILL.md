---
name: dialogflow-cx-to-ces-migration
description: >
  Full production-grade migration of a Dialogflow CX agent (v3beta1) to Google Customer
  Engagement Suite (CES) Conversational Agents. Migrates flows→sub-agents, pages→instructions,
  intents→routing hints, entity types, webhooks→tools, and test cases→golden evaluations CSV.
  Includes retry logic, dry-run mode, and a complete migration report.
metadata:
  openclaw:
    requires:
      bins: ["python", "gcloud"]
      pip: ["google-cloud-dialogflow-cx>=1.28.0", "google-auth"]
---

# Dialogflow CX → CES Migration Skill

## What This Skill Does

Migrates a **Dialogflow CX v3beta1** agent to **Google Customer Engagement Suite (CES) Conversational Agents** format, producing:

| Output File | Contents |
|-------------|----------|
| `ces_agent.json` | CES agent definition (importable via Console or REST API) |
| `golden_evals.csv` | CES batch evaluation CSV (golden test cases) |
| `entity_types.json` | Entity type definitions for manual re-creation |
| `migration_report.md` | Full migration summary with next steps |

## Migration Mapping

| Dialogflow CX | → | CES Conversational Agents |
|---|---|---|
| Agent | → | Agent Application + Root Agent |
| Flow (non-default) | → | Sub-Agent |
| Pages + Routes | → | Agent Instructions (natural language) |
| Intent training phrases | → | Root agent routing hints |
| Entity Types | → | Exported JSON (manual import) |
| Webhook | → | Tool (OpenAPI schema) |
| Form Parameters | → | Instruction slot-filling steps |
| Test Cases | → | Golden Evaluations CSV |

## Prerequisites

1. **GCP Auth**: `gcloud auth application-default login`
2. **Project access**: Dialogflow CX API enabled on the project
3. **Python**: 3.10+
4. **Packages**: `pip install google-cloud-dialogflow-cx google-auth`

## Usage

### Run Migration

```bash
python migrate.py \
  --project YOUR_PROJECT_ID \
  --agent-id YOUR_AGENT_UUID \
  --output ./migration_output
```

### Dry Run (fetch + preview, no files written)

```bash
python migrate.py \
  --project YOUR_PROJECT_ID \
  --agent-id YOUR_AGENT_UUID \
  --dry-run
```

### Custom location (non-global agents)

```bash
python migrate.py \
  --project YOUR_PROJECT_ID \
  --agent-id YOUR_AGENT_UUID \
  --location us-central1 \
  --output ./migration_output
```

## Example (carconnect agent)

```bash
python migrate.py \
  --project genaiguruyoutube \
  --agent-id 3736c564-5b3b-4f93-bbb2-367e7f04e4e8 \
  --output ./carconnect_ces
```

**Expected output:**
- 14 flows → 13 sub-agents + root agent enrichment
- 31 intents → root routing hints
- 5 entity types → exported JSON
- 2 webhooks → 2 OpenAPI tools
- Test cases → golden_evals.csv

## Post-Migration Steps

1. **Review `ces_agent.json`** — check sub-agent instructions make sense, update tool endpoints
2. **Import into CES Console**:
   - Go to [ces.cloud.google.com](https://ces.cloud.google.com)
   - Select project → Import Agent → Upload `ces_agent.json`
3. **Upload Golden Evals**:
   - Evaluate tab → + Add test case → Golden → Upload file → select `golden_evals.csv`
4. **Re-create Entity Types** from `entity_types.json` (CES uses them as tool parameters)
5. **Update webhook endpoints** in the Tools section of your CES agent
6. **Run evaluation suite** → review pass rates → iterate on instructions

## Retry Logic

All Google API calls use exponential backoff (up to 4 attempts, base delay 1.5s × 2ⁿ). If the API is rate-limited or temporarily unavailable, the tool retries automatically.

## Limitations & Known Gaps

- **Rich response types** (carousels, chips, images) are converted to text messages. Update manually in CES.
- **Conditional routes** using session parameter syntax (`$session.params.X`) are preserved as-is in instructions but may need updating for CES parameter syntax.
- **DTMF / telephony settings** are not migrated (CES has different telephony config).
- **Entity type import**: CES does not have a direct batch import API for entity types — use the exported JSON as reference to create them manually or via REST.
- **Webhook auth**: OAuth and mTLS configs are noted but credentials must be re-configured in CES.

## Autoresearch Evals (binary pass/fail)

When running autoresearch on this skill, use these evals:

1. **EVAL_FLOWS**: All non-default flows appear as sub-agents in `ces_agent.json`?
2. **EVAL_TOOLS**: All webhooks appear as tools with OpenAPI schemas in `ces_agent.json`?
3. **EVAL_ENTITIES**: All entity types exported to `entity_types.json`?
4. **EVAL_EVALS_CSV**: `golden_evals.csv` has correct header + at least one golden eval row?
5. **EVAL_INSTRUCTIONS**: Each sub-agent has non-empty instructions?
6. **EVAL_REPORT**: `migration_report.md` exists and contains a stats table?
