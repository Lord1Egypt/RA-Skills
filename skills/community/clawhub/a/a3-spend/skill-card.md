## Description:

Track the owner's spending: record expenses, show weekly or monthly summaries, manage category budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[punyashah](https://clawhub.ai/user/punyashah)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Personal users can ask an OpenClaw assistant to record expenses they state, review weekly or monthly spending by category, and manage monthly category budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and had medium confidence, with a low-probability permissions-scope concern.

Mitigation: Review the requested tool scope and runtime permissions before installing.

Risk: Expense history is stored in a local JSON ledger.

Mitigation: Restrict filesystem access to the ledger and choose a protected location with A3_SPEND_LEDGER.

## Reference(s):

- [Spend Tracker on ClawHub](https://clawhub.ai/punyashah/skills/a3-spend)

## Skill Output:

**Output Type(s):** [Text, JSON files]

**Output Format:** [Plain-text expense summaries and a local JSON expense ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expense amounts are in US dollars; records include dates, categories, merchants, and optional notes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
