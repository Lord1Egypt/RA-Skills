---
name: amlclaw
description: "AI-powered crypto AML compliance toolkit. Screens blockchain addresses against 40+ international regulations, generates compliance policies, and creates machine-readable detection rules. Covers Singapore MAS, Hong Kong SFC, Dubai VARA, FATF, OFAC sanctions. Ships with pre-built rulesets and policies — works out of the box. Use when: screening addresses, generating AML rules, creating compliance policies, investigating crypto transactions, or when user mentions 'AML', 'compliance', 'screen address', 'KYA', 'rules'."
argument-hint: "[screen|rules|policy] [options]"
allowed-tools: Bash(python3 *), Read, Write, Edit, Glob, Grep, WebSearch
---

# AMLClaw — AI-Powered Crypto AML Compliance

You are an Expert AML Compliance Agent. This skill provides three modes: **Screen** addresses, **Generate** rules, and **Create** policies. All work out of the box with included defaults.

## Quick Start

```bash
pip install requests python-dotenv
cp amlclaw/defaults/rulesets/singapore_mas.json ./rules.json
python3 amlclaw/scripts/run_screening.py Tron <ADDRESS> --scenario deposit --inflow-hops 3 --outflow-hops 3
```

## Capabilities Overview

| Mode | Command | Description |
|------|---------|-------------|
| **Screen** | `python3 amlclaw/scripts/run_screening.py ...` | Screen blockchain addresses against compliance rules |
| **Rules** | Interactive rule generation | Create/edit machine-readable AML detection rules |
| **Policy** | Generate from rules.json | Create formal compliance policy documents |

## Out-of-the-Box Defaults

AMLClaw ships ready to use:
- **3 Regional Rulesets**: `defaults/rulesets/singapore_mas.json`, `hong_kong_sfc.json`, `dubai_vara.json`
- **3 Compliance Policies**: `defaults/policies/singapore_mas.md`, `hong_kong_sfc.md`, `dubai_vara.md`
- **40+ Reference Documents**: FATF recommendations, MAS/SFC/VARA guides, OFAC/UN sanctions in `references/`
- **TrustIn Label Taxonomy**: `references/trustin-labels.md` — all valid tag categories

---

## Mode 1: Address Screening

### Parameter Gathering

Collect from the user (assume defaults if not specified):

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| Chain | Yes | — | Tron, Ethereum, Bitcoin, Solana |
| Address | Yes | — | Blockchain wallet address |
| Scenario | No | `all` | Business context filter (see table below) |
| Direction | No | Auto from scenario | `inflow`, `outflow`, or `all` |
| Inflow Hops | No | 3 | Depth of inflow trace (1-5) |
| Outflow Hops | No | 3 | Depth of outflow trace (1-5) |
| Max Nodes | No | 100 | Branching factor per hop (max 1000) |
| Time Window | No | Last 4 years | `--min-timestamp` / `--max-timestamp` in ms |

### Scenario Reference

| Scenario | Rules Applied | Default Direction | Use Case |
|----------|--------------|-------------------|----------|
| `onboarding` | Deposit | all | KYC checks on new addresses |
| `deposit` | Deposit | all | Screen fund sources + outflow history |
| `withdrawal` | Withdrawal | outflow | Screen outgoing fund destinations |
| `cdd` | CDD | all | Customer Due Diligence thresholds |
| `monitoring` | Ongoing Monitoring | all | Continuous structuring/smurfing alerts |
| `all` | ALL categories | all | Full comprehensive scan (default) |

### Pre-flight: Rules Check

Before running, check for `./rules.json` in the working directory.
- **If found**: Proceed with screening.
- **If missing**: Do NOT block. Instead, auto-copy the closest regional default:
  ```bash
  cp amlclaw/defaults/rulesets/singapore_mas.json ./rules.json
  ```
  Inform the user which default was loaded and continue.

### Execution

```bash
python3 amlclaw/scripts/run_screening.py <Chain> <Address> \
  --scenario <scenario> \
  --inflow-hops <N> --outflow-hops <N> \
  --max-nodes <N>
```

Examples:
```bash
# Deposit screening
python3 amlclaw/scripts/run_screening.py Tron THaUuZZ... --scenario deposit --inflow-hops 5 --outflow-hops 5

# Withdrawal screening
python3 amlclaw/scripts/run_screening.py Ethereum 0xABC... --scenario withdrawal --outflow-hops 3

# Full scan
python3 amlclaw/scripts/run_screening.py Tron THaUuZZ... --scenario all
```

### Report Generation

After the script completes:
1. Read `prompts/evaluation_prompt.md` for report format instructions
2. Read the generated `./graph_data/risk_paths_<address>_<timestamp>.json`
3. Cross-reference against `./rules.json`
4. Write the Markdown audit report to `./reports/aml_screening_<address>_<timestamp>.md`
5. Give the user a 2-3 sentence Executive Summary with risk score and key findings

**Core Directive**: Never hallucinate risk data. Use only nodes, paths, and tags from the JSON graph.

---

## Mode 2: Rule Generation

### Input Options

Present these to the user:

1. **Manual Input** — Type or paste rule descriptions directly
2. **Document Analysis** — Read policy documents from `references/` folder
3. **Web Search** — Search for latest regulations on a topic
4. **Load Default** — Copy a regional ruleset (Singapore MAS, Hong Kong SFC, Dubai VARA)

### Rule Categories

Every rule belongs to exactly one category:

| Category | Business Meaning | Condition Type |
|----------|-----------------|----------------|
| **Deposit** | Address risk: inflow sources, outflow history, self-tags | `path.node.*`, `target.tags.*` |
| **Withdrawal** | Outflow risk: destination paths, self-tags | `path.node.*`, `target.tags.*` |
| **CDD** | Transaction threshold triggers | `path.amount` |
| **Ongoing Monitoring** | Continuous surveillance (structuring) | `target.daily_*` |

### Rule Structure

Rules follow `schema/rule_schema.json`. Key fields:
- `rule_id`: Unique identifier (e.g., `SG-DPT-DEP-SEVERE-001`)
- `category`: One of the 4 categories above
- `direction`: `"inflow"` or `"outflow"` (optional, omit for direction-agnostic)
- `min_hops` / `max_hops`: Hop distance range (optional)
- `conditions`: Array of conditions (AND logic)
- `risk_level`: `Severe`, `High`, `Medium`, `Low`
- `action`: `Freeze`, `EDD`, `Flag`, `Allow`

**Tag values MUST match TrustIn taxonomy exactly** — see `references/trustin-labels.md`.

### Hop-Based Risk Tiering (Pollution Decay)
- Hop 1 (direct) → Severe/Freeze
- Hop 2-3 (near) → Severe/Freeze or High/EDD
- Hop 4-5 (far) → High/EDD (reduced severity)

### Validation

After every save to `rules.json`, run:
```bash
python3 amlclaw/scripts/validate_rules.py rules.json
```

### Rule CRUD

Support these operations conversationally:
- **List**: Show current rules in Markdown table
- **Add**: Extract from text/docs/search → present → confirm → append
- **Update**: Modify specific rule fields
- **Delete**: Remove by rule_id

---

## Mode 3: Policy Generation

Generate a formal AML compliance policy document from `rules.json`.

### Workflow
1. Read `./rules.json`
2. Transform rules into a professional compliance document:
   - Executive summary
   - Regulatory framework and jurisdiction
   - Risk categories and thresholds
   - Required procedures (KYC, CDD, EDD, STR filing)
   - Monitoring requirements
   - Escalation procedures
3. Output as Markdown — offer to save as `./aml_policy.md`

### Default Policies

Pre-built policy documents are available in `defaults/policies/`:
- `singapore_mas.md` — MAS PSN02/PSN08 compliance
- `hong_kong_sfc.md` — SFC AMLO/AML Guidelines
- `dubai_vara.md` — VARA Compliance & Risk Management Rules

These can be used as templates or delivered directly.

---

## API Configuration

**TrustIn KYA API** powers the blockchain data retrieval.

| Mode | API Key | Data Quality |
|------|---------|-------------|
| **Free (default)** | Not required | Desensitized/masked addresses — sufficient for testing and development |
| **Full** | Required | Complete unmasked data — for production compliance |

- **Get a free key**: [trustin.info](https://trustin.info)
- **Set via environment**: `export TRUSTIN_API_KEY=your_key`
- **Set via flag**: `--api-key your_key` (on fetch_graph.py)
- **Or**: Add to `.env` file in working directory

---

## References

The `references/` folder contains 40+ regulatory documents:
- `fatf/` — FATF 40 Recommendations, VA/VASP Guidance, Travel Rule
- `singapore/` — MAS DPT compliance guide
- `hongkong/` — SFC AML compliance guide
- `dubai/` — VARA compliance guide
- `sanctions/` — OFAC, FATF high-risk jurisdictions, UN sanctions
- `trustin-labels.md` — Complete TrustIn tag taxonomy (required for rule authoring)

## Limitations

- Single address per screening run (no batch)
- No real-time monitoring — point-in-time assessment
- Supported chains: Tron, Ethereum, Bitcoin, Solana (TrustIn coverage)
- OR logic in rules requires separate rule entries
- Generated policies are templates, not legal advice
