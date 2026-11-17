## Description:

Persistent memory for agents across sessions, machines, sandboxes, and agent platforms, stored in a private DataEcho cloud drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohocp](https://clawhub.ai/user/mohocp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to recall, create, update, remove, recover, and hand off durable agent memories stored in DataEcho cloud storage. It is intended for preferences, decisions, milestones, project-scoped facts, and cross-session context rather than secrets or transient notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved memories persist outside the agent session in DataEcho cloud storage.

Mitigation: Store only durable, non-sensitive preferences, decisions, milestones, and project facts; do not store secrets, API keys, regulated personal data, or confidential business information.

Risk: Writable handoff tokens can let another agent change shared memory.

Mitigation: Prefer read-only handoff tokens and require explicit user confirmation before issuing writable tokens.

Risk: Memories can become stale or incorrect over time.

Mitigation: Verify file paths, URLs, flags, and dated facts before acting on recalled memories, and remove or update false memories promptly.

## Reference(s):

- [Server-resolved source repository](https://github.com/mohocp/dataecho/tree/main/skills/dataecho-memory)
- [DataEcho homepage](https://dataecho.ai)
- [DataEcho LLM documentation](https://dataecho.ai/llms-full.txt)
- [DataEcho OpenAPI specification](https://dataecho.ai/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include memory recall results, memory write/update instructions, handoff token setup steps, and recovery commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
