## Description:

Personal finance assistant that queries local Hapoalim, Isracard, and Max SQLite databases to answer questions about transactions, merchants, subscriptions, monthly summaries, income, and spending patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharon8811](https://clawhub.ai/user/sharon8811)

### License/Terms of Use:

MIT-0

## Use Case:

Users with AccountantPriv SQLite exports use this skill to answer personal finance questions, locate recurring charges, summarize monthly income and expenses, and analyze spending patterns. The skill is intended for agents that can run local helper scripts against the user's finance databases and report concise findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive bank and credit card transaction data in agent outputs.

Mitigation: Use it only for expected personal finance tasks, avoid sharing raw outputs externally, and mask account or card identifiers in documentation and responses.

Risk: The raw SQL helper can run unrestricted database statements and may modify or damage finance databases.

Mitigation: Make database access read-only or remove the raw SQL helper before routine use; prefer constrained merchant lookup and monthly summary tools.

Risk: Monthly summaries may be misleading while the month/year parsing issue identified by security evidence remains unresolved.

Mitigation: Verify requested month and year values against source transactions before relying on reported totals.

## Reference(s):

- [Database Schemas - AccountantPriv](references/schema.md)
- [ClawHub skill page](https://clawhub.ai/sharon8811/skills/accountant-priv-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Analysis]

**Output Format:** [Markdown or plain-text financial answers, with JSON output from helper scripts when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive transaction details, dates, amounts, merchant names, account or card identifiers, and Hebrew-language responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
