## Description:

Manage FoxReach cold email outreach - leads, campaigns, sequences, templates, email accounts, inbox, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[concaption](https://clawhub.ai/user/concaption)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage FoxReach outreach operations, including leads, campaigns, sequences, templates, email accounts, inbox triage, and analytics through the FoxReach Python SDK or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live data-changing outreach actions, including creating, updating, deleting, assigning, and starting campaigns.

Mitigation: Require explicit user approval before any state-changing operation or action that could send real email.

Risk: FoxReach API keys could be exposed through pasted source, command history, or shared examples.

Mitigation: Use environment variables or a secret manager for credentials and avoid hardcoding or pasting API keys into scripts.

Risk: Production campaign examples could send email before a campaign, lead list, sender account, or sequence is reviewed.

Mitigation: Review campaign settings, recipients, sender accounts, and sequence content before assigning accounts or starting a campaign.

## Reference(s):

- [FoxReach API Reference](api-reference.md)
- [FoxReach SDK Examples](examples.md)
- [FoxReach Skill Page](https://clawhub.ai/concaption/skills/foxreach-io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FoxReach API key for live API operations; should present concise summaries instead of raw JSON by default.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
