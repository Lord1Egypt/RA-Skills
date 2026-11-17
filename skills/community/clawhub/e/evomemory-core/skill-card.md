## Description:

Evomemory Core provides a local memory system for OpenClaw AI agents with ChromaDB and LanceDB support, hybrid retrieval, semantic deduplication, auto-classification, and Chinese semantic retrieval optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulan3954-a11y](https://clawhub.ai/user/lulan3954-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent builders use this skill to add local memory, vector retrieval, and migration support to OpenClaw-compatible agents. It is suited for workflows that need offline memory storage with optional ChromaDB or LanceDB backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote ChromaDB configuration can transmit memory data, queries, metadata, and an API key despite offline-only positioning.

Mitigation: Use local ChromaDB by default; configure remote servers only when they are trusted and protected with secure transport.

Risk: API keys may be placed in ordinary configuration.

Mitigation: Store secrets outside plain project config when possible and restrict access to any configuration that contains credentials.

Risk: Migration or deletion operations can affect important memory data.

Mitigation: Back up memory stores before migration, deletion, or backend-switching operations.

Risk: Dependency installation may introduce unpinned packages into a shared Python environment.

Mitigation: Install in a dedicated environment and pin dependency versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lulan3954-a11y/skills/evomemory-core)
- [Publisher profile](https://clawhub.ai/user/lulan3954-a11y)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code, shell commands, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup and integration guidance for an OpenClaw memory extension.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
