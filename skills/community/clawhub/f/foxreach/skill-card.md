## Description:

Manage FoxReach cold email outreach -- leads, campaigns, sequences, templates, email accounts, inbox, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[concaption](https://clawhub.ai/user/concaption)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage a real FoxReach cold email outreach workspace, including leads, campaigns, sequences, templates, inbox triage, email accounts, and analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on live outreach data and campaigns.

Mitigation: Install it only for intended FoxReach workspaces and require explicit user confirmation before deletes, account changes, or starting campaigns that send email.

Risk: API keys may be exposed if pasted directly into commands, scripts, or chat history.

Mitigation: Use FOXREACH_API_KEY from the environment or a secret manager, and avoid embedding keys in reusable code or command examples.

Risk: Cold email campaign actions can send external messages or alter recipient records.

Mitigation: Review lead lists, sequence content, sender accounts, and campaign settings before executing send-related actions.

## Reference(s):

- [FoxReach API Reference](artifact/api-reference.md)
- [FoxReach SDK Examples](artifact/examples.md)
- [Foxreach on ClawHub](https://clawhub.ai/concaption/skills/foxreach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute FoxReach API operations when supplied with a valid FOXREACH_API_KEY.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
