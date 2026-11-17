## Description:

Guides agents in creating, reading, replying to, and deleting temporary AgentMail inboxes through API calls, shell commands, Python snippets, and the AgentMail web console.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjotrglushkov-byte](https://clawhub.ai/user/pjotrglushkov-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate workflows that need temporary email inboxes, including account verification, inbox polling, message review, replies, and cleanup through AgentMail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains a live-looking AgentMail API key and related email configuration.

Mitigation: Treat the key as compromised, rotate it before use, and replace packaged secrets with environment-variable or secret-manager instructions.

Risk: The skill references Python scripts outside the package that were not included for review.

Mitigation: Include the scripts in the package or pin them by verified hashes before users run the commands.

Risk: Email automation can expose sensitive message content.

Mitigation: Use an isolated environment and avoid sensitive email content until the security issues identified by evidence.security are fixed.

## Reference(s):

- [AgentMail quickstart documentation](https://docs.agentmail.to/quickstart)
- [AgentMail documentation](https://agentmail.to/docs)
- [AgentMail web console](https://console.agentmail.to)
- [ClawHub skill page](https://clawhub.ai/pjotrglushkov-byte/skills/agentmail-to)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AgentMail API requests, browser-use commands, and environment variable setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
