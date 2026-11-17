## Description:

Felo SuperAgent lets agents run Felo Open Platform SuperAgent conversations with SSE streaming, persistent LiveDoc context, follow-up threads, brand styles, and generated assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to Felo SuperAgent for multi-turn chat, LiveDoc-associated work, logo or product image generation, and tool-augmented answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, prior conversation context, LiveDoc/thread IDs, selected resources, and style data may be sent to Felo.

Mitigation: Install only when this data sharing is acceptable, and start a new LiveDoc or thread when switching projects or sensitive topics.

Risk: The FELO_API_KEY credential can be exposed if stored permanently in a shared or synced shell profile.

Mitigation: Prefer temporary environment configuration on shared systems and rotate the key if exposure is suspected.

Risk: Setting FELO_API_BASE can redirect requests, prompts, credentials, and state to a non-default endpoint.

Mitigation: Do not set FELO_API_BASE unless the exact endpoint is fully trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/felo-superagent)
- [SuperAgent API Documentation](https://openapi.felo.ai/docs/api-reference/v2/superagent.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [Get API Key](https://felo.ai)
- [Felo Skills Repository](https://github.com/Felo-Inc/felo-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON with answer text, LiveDoc/thread state, image URLs, and generated artifact titles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include LiveDoc links, image URLs, research/document/PPT/HTML titles, and Twitter/X search results; requires FELO_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
