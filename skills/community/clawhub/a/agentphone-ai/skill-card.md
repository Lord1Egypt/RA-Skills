## Description:

Get your AI agent a real US/Canada phone number in one API call. Make voice calls, send and receive SMS, and hold actual conversations via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modi2meet](https://clawhub.ai/user/modi2meet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to connect agents to AgentPhone so they can provision phone numbers, send and receive SMS, place voice calls, manage agent settings, configure webhooks, and retrieve call or message history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable live calls, SMS, and billable account actions.

Mitigation: Use it only with explicit permission for each person or business contacted, confirm costly or irreversible actions before execution, and monitor account usage.

Risk: Phone numbers, messages, call recordings, and transcripts may contain sensitive personal data.

Mitigation: Limit collection and sharing to the intended task, avoid storing sensitive content in persistent agent memory, and configure webhooks only to trusted endpoints.

Risk: An exposed AgentPhone API key can let another party impersonate the account and incur charges.

Mitigation: Store API keys in environment variables or a secrets manager, never paste them into chat, and rotate any key that may have been exposed.

## Reference(s):

- [AgentPhone homepage](https://agentphone.to)
- [AgentPhone documentation](https://docs.agentphone.to)
- [AgentPhone API base](https://api.agentphone.to)
- [AgentPhone MCP Tools Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API requests that create accounts, provision phone numbers, send SMS, place calls, configure webhooks, and retrieve transcripts.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
