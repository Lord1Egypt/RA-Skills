## Description:

Aoineco Ledger helps agents track AI operating expenses, revenue, budgets, ROI, runway, and per-agent cost attribution with a zero-dependency Python ledger engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add local financial tracking for AI agent workloads, including API costs, gas fees, revenue, budgets, bootstrap runway, ROI, and CSV or JSON exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used with sensitive financial records stored in local plaintext files.

Mitigation: Treat ledger files as sensitive local records, restrict filesystem access, and do not assume encryption is provided by the skill.

Risk: Budget warnings may be mistaken for hard spending enforcement.

Mitigation: Use the budget checks as alerts only, and add independent enforcement before relying on them for real spending controls.

Risk: The release overstates protections for financial data and budget controls.

Mitigation: Review the implementation and security guidance before using it for real spending decisions or financial recordkeeping.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/aoineco-ledger)
- [Publisher profile](https://clawhub.ai/user/edmonddantesj)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, JSON, CSV]

**Output Format:** [Markdown guidance with Python code snippets; ledger reports and exports can be returned as JSON, CSV, or plain text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON and JSONL files for ledger state; no external Python dependencies are required.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
