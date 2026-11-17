## Description:

Connects agents to the AI_Health acupoint wellness MCP service for traditional Chinese medicine acupoint massage consultations, share retrieval and creation, reference-book listing, and multi-turn clarification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengkane](https://clawhub.ai/user/dengkane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent or MCP client to AI_Health for acupoint massage guidance, follow-up clarification, source-book lookup, and optional sharing of consultation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill derives a stable client ID from local machine identity, hostname, and username, then uses that ID with health consultation content.

Mitigation: Review the tracking behavior before installation, inform users before use, and avoid deployment where persistent device-linked health histories are not acceptable.

Risk: Shared consultation conversations may become accessible through a generated share link.

Mitigation: Use share_create only for conversations intended to be shared, and avoid creating shares for sensitive health discussions.

Risk: The skill provides wellness-oriented acupoint guidance that may be mistaken for medical advice.

Mitigation: Preserve the service's final-answer disclaimers and direct users to qualified medical care for urgent, severe, or uncertain symptoms.

## Reference(s):

- [AI_Health MCP service](https://health.geeyo.com)
- [AI_Health Streamable HTTP MCP endpoint](https://health.geeyo.com/mcp)
- [AI_Health legacy SSE MCP endpoint](https://health.geeyo.com/mcp/sse)
- [Protocol examples](references/protocol_examples.md)
- [ClawHub skill page](https://clawhub.ai/dengkane/skills/acupoint-health-tool)
- [ClawHub publisher profile](https://clawhub.ai/user/dengkane)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return health consultation content, follow-up prompts, cited classical text references, share identifiers, and MCP configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
