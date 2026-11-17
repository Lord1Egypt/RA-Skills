## Description:

Connect Claude to external apps like Gmail, Slack, GitHub. Use this skill when the user wants to send emails, create issues, post messages, or take actions in external services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect Claude Code to third-party apps through Composio Tool Router and request actions such as sending email, creating issues, posting messages, and updating documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and authorize a broad third-party tool that can perform real actions in connected apps.

Mitigation: Install only if the user trusts the composio-toolrouter plugin source, use narrow OAuth scopes where available, and confirm each live action before execution.

Risk: Connected-app actions can affect external services such as email, Slack, GitHub, and Notion.

Mitigation: Review the target app, recipient or destination, and action content before execution, and know how to revoke the API key and app authorizations.

## Reference(s):

- [Composio Platform](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills)
- [ClawHub Skill Page](https://clawhub.ai/sohamganatra/skills/connect-apps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide live actions in connected external apps after user authorization.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
