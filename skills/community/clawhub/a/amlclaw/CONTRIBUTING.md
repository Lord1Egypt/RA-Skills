# Contributing to AMLClaw

This guide is for AI agents (Claude Code, OpenClaw, etc.) contributing to this repo.

## Adding New Regulations

1. Place `.md` files in `references/<jurisdiction>/`
2. Follow naming convention: `<ID>-<Short-Title>.md` (e.g., `FATF-001-40-Recommendations-2025.md`)
3. Include source URL, effective date, and key provisions
4. Reference documents are used by agents to generate rulesets and policies

## Adding New Regional Rulesets

1. Create a JSON file in `defaults/rulesets/<jurisdiction>.json`
2. Follow the schema in `schema/rule_schema.json`
3. Each rule must have:
   - `rule_id`: Format `<COUNTRY>-<REGULATOR>-<CATEGORY>-<LEVEL>-<SEQ>` (e.g., `SG-DPT-DEP-SEVERE-001`)
   - `category`: One of `Deposit`, `Withdrawal`, `CDD`, `Ongoing Monitoring`
   - `conditions`: Array of parameter/operator/value objects
   - `risk_level`: `Severe`, `High`, `Medium`, or `Low`
   - `action`: `Freeze`, `Reject`, `EDD`, `Review`, `Allow`, or `Whitelist`
   - `reference`: Cite the specific regulation section
4. Use tag categories from `references/trustin-labels.md`

## Adding New Policy Documents

1. Create a `.md` file in `defaults/policies/<jurisdiction>.md`
2. Reference actual rule IDs from the corresponding ruleset
3. Cover: CDD/EDD, screening procedures, STR filing, record keeping, Travel Rule, sanctions, monitoring

## Validation

Before submitting, validate your ruleset:

```bash
python3 scripts/validate_rules.py defaults/rulesets/<your_file>.json
```

Validation must pass with zero errors.

## PR Expectations

- All rulesets validate cleanly
- Follow existing naming conventions and file structure
- Reference specific regulation sections (not generic citations)
- One jurisdiction per PR preferred
- Policy documents should reference rule IDs from the paired ruleset
