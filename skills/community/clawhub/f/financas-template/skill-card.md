## Description:

Manages personal finances with categorized expense and income tracking, bank and card statement processing, and monthly or annual summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evandrotho](https://clawhub.ai/user/evandrotho)

### License/Terms of Use:

MIT-0

## Use Case:

Personal finance users and their agents use this skill to maintain workspace-based finance records, add confirmed transactions, process uploaded bank or card statements, and answer spending or balance questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and analyzes sensitive personal finance files in the workspace.

Mitigation: Install it only in workspaces where the agent may access finance files and uploaded bank or card statements.

Risk: Broad finance-related triggers may activate the skill during unrelated requests.

Mitigation: Review activation carefully and decline or redirect the agent when the request is not a finance task.

Risk: Incorrect transaction interpretation could produce inaccurate ledger updates.

Mitigation: Check the transaction summary, duplicate warnings, date, category, value, and payment method before confirming writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evandrotho/skills/financas-template)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown finance records and text confirmations or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before writing transaction records and checks for likely duplicates before adding entries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
