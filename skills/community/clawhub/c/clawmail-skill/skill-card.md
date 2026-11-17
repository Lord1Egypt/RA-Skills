## Description:

Email infrastructure for autonomous AI agents. Create inboxes, send/receive emails, no human intervention required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claw-mail](https://clawhub.ai/user/claw-mail)

### License/Terms of Use:


## Use Case:

Developers and agent builders use ClawMail to give autonomous agents email inboxes, send and receive messages, manage mailbox state, and complete required Twitter/X verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants authority to send, read, modify, and delete an agent mailbox.

Mitigation: Install only when that mailbox authority is acceptable for the agent's use case, and reserve destructive delete operations for explicit intent.

Risk: Credential exposure could allow another party to impersonate the agent.

Mitigation: Store the API key in a secret manager or locked-down file, keep it out of agent memory and logs, and send it only to https://api.clawmail.to.

Risk: The TypeScript client introduces a package dependency into agent projects.

Mitigation: Pin and review the npm client version before installation.

## Reference(s):

- [ClawMail Skill Page](https://clawhub.ai/claw-mail/skills/clawmail-skill)
- [ClawMail Website](https://clawmail.to)
- [ClawMail Skill Source](https://clawmail.to/skill.md)
- [ClawMail Package Metadata](https://clawmail.to/skill.json)
- [ClawMail API](https://api.clawmail.to)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with curl commands, JSON examples, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ClawMail API keys and mailbox operations against https://api.clawmail.to.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
