## Description:

Give your AI agent a soul: beliefs, values, voice, and boundaries that persist across every conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to the Live Neon platform for persistent identity, belief, responsibility, voice, and boundary management across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload conversation-derived observations or content to Live Neon.

Mitigation: Use only non-sensitive conversations and content unless the organization has approved Live Neon as a data processor; avoid source_quote uploads that may contain private data.

Risk: Fetched identity or prompt text is remotely mutable and may be used as agent context.

Mitigation: Review fetched identity text before use and keep existing platform, system, developer, and safety instructions higher priority.

Risk: Bulk approval and recurring heartbeat workflows can quickly promote or refresh identity traits.

Mitigation: Avoid --approve-all for unreviewed items and enable scheduled jobs only with clear consent, scoped tokens, logging, rollback, and retention or deletion plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liveneon/skills/agent-soul-manager)
- [Publisher profile](https://clawhub.ai/user/liveneon)
- [Live Neon Agent platform](https://persona.liveneon.ai)
- [Live Neon homepage](https://liveneon.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Live Neon API token and can return identity text for agent context.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
