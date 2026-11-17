## Description:

AOMS provides a persistent local memory service for AI agents with tiered memory, weighted retrieval, optional vector search, progressive disclosure, and HTTP APIs for recall and updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhawala4](https://clawhub.ai/user/dhawala4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to a long-lived local memory service for task recall, knowledge capture, weighted search, and optional OpenClaw integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill introduces long-lived, mutable local memory that may persist sensitive or stale agent context.

Mitigation: Use it only when persistent memory is intended, avoid storing secrets or regulated data, and periodically review stored memories.

Risk: A local HTTP memory service can expose agent memory if bound too broadly or deployed without access controls.

Mitigation: Bind the service to 127.0.0.1 and add authentication or network isolation before broader deployment.

Risk: Migration and ingestion features can import unwanted or sensitive source material into persistent memory.

Mitigation: Review migration and ingestion inputs first, and use dry-run or explicit opt-in flows before committing imports.

Risk: Recalled memories can be outdated, incorrect, or adversarial if treated as instructions.

Mitigation: Treat recalled memories as untrusted notes and require the agent or user to validate them before acting.

## Reference(s):

- [AOMS API Reference](references/api-reference.md)
- [OpenClaw Setup](references/openclaw-setup.md)
- [ClawHub Skill Page](https://clawhub.ai/dhawala4/skills/aoms)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash, Python, YAML, HTTP API examples, and optional JSON responses from the memory service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt-ready recall context and instructions for writing, searching, reinforcing, migrating, and maintaining local agent memory.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
