## Description:

Manage email inboxes and messages via AgentMail API. Create disposable inboxes, send/receive emails, and list messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stepandel](https://clawhub.ai/user/stepandel)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure AgentMail CLI access, create temporary inboxes, send messages, list received messages, and retrieve or delete email through the AgentMail API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AgentMail API key and can store it in a local configuration file.

Mitigation: Use a scoped or temporary AGENTMAIL_API_KEY when possible, avoid persistent storage on shared machines, and confirm credential handling before use.

Risk: The skill can send email and delete inboxes or messages, including deleting the thread that contains a message.

Mitigation: Require explicit confirmation before sending email or deleting inboxes or messages.

Risk: The skill depends on installing and trusting the third-party npm package @stepandel/agentmail-cli.

Mitigation: Install only when the npm package source is trusted for the deployment environment.

## Reference(s):

- [AgentMail](https://agentmail.to)
- [agentmail-cli ClawHub Skill](https://clawhub.ai/stepandel/skills/agentmail-cli)
- [agentmail-cli npm package](https://www.npmjs.com/package/@stepandel/agentmail-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands generally require the agentmail binary and AGENTMAIL_API_KEY; the skill recommends --json for machine-readable command output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
