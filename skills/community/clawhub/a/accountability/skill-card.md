## Description:

Tracks operational follow-ups for actions with future outcomes, including deploys, cron changes, fixes, configuration changes, verification checks, escalation, and audit archival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to register, verify, escalate, and close follow-ups for operational actions that need later confirmation. It is intended for workflows where deployment, cron, infrastructure, data, or integration changes should be tracked until the outcome is known.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run free-form checks recorded in project notes, including checks that use network access or credentials.

Mitigation: Review every stored Check command before it runs, prefer structured check types over shell snippets, and require explicit approval before networked or credentialed checks execute.

Risk: The skill automatically changes operational follow-up and audit files.

Mitigation: Treat FOLLOWUPS.md as trusted operational input, restrict who can edit it, and review changes to follow-up and archive records.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown ledger entries and concise text summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains follow-up and archive records for operational verification workflows.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
