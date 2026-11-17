## Description:

Earn up to 70% revenue share when your agent naturally recommends relevant products. Powered by AgentLoop — the agentic marketing network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smjai](https://clawhub.ai/user/smjai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to check recent conversation context and draft responses with AgentLoop for relevant sponsored product mentions before finalizing an agent response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversation context and draft agent responses are sent to an external marketing service.

Mitigation: Use only where users can be told about the behavior and where sending conversation context to AgentLoop is acceptable.

Risk: The bundled redaction is pattern-based and does not reliably detect free-form sensitive content.

Mitigation: Do not invoke the skill for sensitive, medical, legal, financial, confidential, or crisis conversations unless stronger local filtering and consent controls are added.

Risk: The skill can append remote sponsored mention text to an agent response.

Mitigation: Keep the sponsored disclosure, enforce the one-mention-per-conversation limit, and review use against the agent owner's advertising policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smjai/skills/agentloop)
- [AgentLoop homepage](https://agentloop.life)
- [AgentLoop documentation](https://agentloop.life/docs)
- [AgentLoop check API endpoint](https://agentloop.life/api/sdk/check)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [JSON from the check script plus optional sponsored mention text for the agent response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTLOOP_API_KEY and sends pattern-redacted recent conversation context, draft response, and hashed user ID to AgentLoop.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
