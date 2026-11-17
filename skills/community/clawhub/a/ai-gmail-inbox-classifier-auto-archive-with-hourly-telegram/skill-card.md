## Description:

Automatically organizes Gmail inbox messages hourly by reading each new message, classifying it into Gmail labels, archiving processed inbox messages, and sending Telegram alerts for messages labeled Important.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, professionals, and teams use this skill to automate Gmail inbox triage, label assignment, archiving, and Important-message Telegram alerts through AgentPMT-hosted workflow tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads Gmail messages, searches sent mail, applies labels, archives processed inbox messages, and sends Telegram alerts.

Mitigation: Confirm the Gmail and Telegram scopes, workflow settings, and account connections before using real mailboxes.

Risk: The security evidence notes mutable, unpinned external installs for a workflow that handles sensitive email.

Mitigation: Prefer pinned or verified dependency installation and review the skill before deployment.

Risk: Every processed inbox message may be archived by the automation.

Mitigation: Test with a non-critical account or limited inbox scope before enabling the workflow on production mail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram)
- [AgentPMT workflow page](https://www.agentpmt.com/agent-workflow-skills/ai-gmail-inbox-classifier-auto-archive-with-hourly-telegram-alerts)
- [AgentPMT publisher profile](https://clawhub.ai/user/agentpmt)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Gmail - All Email Actions](https://clawhub.ai/agentpmt/gmail-all-email-actions)
- [Telegram Instant Messenger](https://clawhub.ai/agentpmt/telegram-instant-messenger)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown, JSON]

**Output Format:** [Markdown instructions with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides AgentPMT workflow calls that read Gmail messages, apply labels, archive processed inbox messages, and send Telegram alerts.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
