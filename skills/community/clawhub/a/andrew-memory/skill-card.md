## Description:

Andrew Memory Layer is a semantic long-term memory skill for AI agents that uses LanceDB to store and search memories, manage Core Identity, and distill conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panyuugit](https://clawhub.ai/user/panyuugit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an OpenClaw agent persistent memory, semantic recall, Core Identity retrieval, and conversation distillation across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory text, search queries, and conversation transcripts may be sent to MiniMax or to a configured local LLM endpoint.

Mitigation: Prefer local mode for sensitive use, keep localLlmUrl restricted to a trusted loopback Ollama service, and avoid storing secrets or regulated data.

Risk: The skill can persist long-term memories and update Core Identity without a clear approval boundary.

Mitigation: Require human review before identity changes, vector regeneration, or storing sensitive memories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panyuugit/skills/andrew-memory)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Plain text tool responses with JSON-like tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores durable LanceDB memory and Core Identity records in the configured data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
