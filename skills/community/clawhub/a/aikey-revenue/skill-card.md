## Description:

Analyzes revenue changes for owner-operators by separating customer count, per-customer volume, and price, while checking for hidden group shifts and gradual declines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Owner-operators use this skill to understand whether a revenue change came from customer numbers, customer purchasing volume, or price. It works from ledger or order-book data and returns an evidence-based attribution with follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential customer names, financial values, or payment patterns may persist in the skill’s memory.

Mitigation: Review where memory is stored and who can access it; omit sensitive details from memory and remove existing notes when they should not persist.

## Reference(s):

- [Revenue attribution theory notes](references/理论底座.md)
- [ClawHub skill page](https://clawhub.ai/iamzifei/skills/aikey-revenue)
- [AI KEY rename and upgrade notes](https://github.com/iamzifei/aikey#老用户升级zmm-已改名为-ai-key)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with tables and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Attribution detail depends on the period, business definitions, and transaction detail supplied.]

## Skill Version(s):

0.2.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
