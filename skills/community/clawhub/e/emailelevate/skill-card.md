## Description:

Automates email campaigns, sequences, and analytics for small businesses, including drip campaigns, welcome series, performance tracking, and integrations with Mailchimp, ConvertKit, and ActiveCampaign.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Small business owners, marketers, agencies, and consultants use this skill to plan, launch, automate, and analyze email marketing workflows across common email-service providers. It is intended for campaigns, welcome sequences, segmentation, reporting, template guidance, and related configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to use marketing-service credentials and may access customer or subscriber data.

Mitigation: Configure only the provider key needed for the task, prefer least-privilege tokens, and avoid exposing unrelated marketing accounts or datasets.

Risk: The skill describes high-impact external actions such as sending campaigns, changing lists or tags, syncing CRM or ecommerce data, exporting reports, and posting to Slack.

Mitigation: Require explicit human approval before any external send, data mutation, data export, CRM or ecommerce sync, or Slack notification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/emailelevate)
- [Publisher profile](https://clawhub.ai/user/ncreighton)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, shell-command, workflow-diagram, and analytics-report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include email campaign plans, sequence structures, segmentation logic, template guidance, configuration examples, and reporting recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
