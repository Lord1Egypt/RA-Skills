## Description:

Routes messages from specified Feishu group chats to corresponding agents for processing and relays their replies back to the original group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunitaly](https://clawhub.ai/user/sunitaly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace operators use this skill to route incoming messages from configured group chats to designated sub-agents and relay those agents' responses back to the originating group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Group messages are automatically sent to sub-agents and replies are forwarded back to Feishu without clearly documented safeguards.

Mitigation: Limit the skill to intended groups and least-privilege sub-agents, validate senders, and require review before forwarding sensitive or high-impact responses.

Risk: Untrusted or sensitive chat content may be exposed to the wrong agent or returned to the wrong group.

Mitigation: Treat group messages as untrusted data, preserve the originating chat context, and redact sensitive content where possible before delegation or relay.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sunitaly/skills/feishu-routing)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or plain text instructions, with delegated agent replies relayed as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes by configured Feishu chat_id values and forwards sub-agent replies through the main agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
