## Description:

One-click clone of a production-grade semantic memory system: HOT/WARM/COLD tiered storage + Qdrant vector DB + Neo4j graph DB + qwen3-embedding. Enables cross-session semantic retrieval and entity relationship memory for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local, cross-session semantic memory to AI agent workflows using tiered files, vector search, graph relationships, and local embeddings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts persistent local Qdrant and Neo4j services that may expose stored agent memory if left unauthenticated or reachable beyond localhost.

Mitigation: Bind database ports to localhost, enable authentication for Neo4j and Qdrant, restrict network access, and stop the containers when not in use.

Risk: Agent memory stores may retain sensitive prompts, preferences, decisions, or project context across sessions.

Mitigation: Review what will be stored before use and keep a documented process to delete memory files and Docker volumes.

Risk: The setup uses external container images and an embedding model whose versions may change over time.

Mitigation: Pin container and model versions, review updates before deployment, and validate the setup in a controlled environment.

## Reference(s):

- [Deep Memory ClawHub Skill Page](https://clawhub.ai/halfmoon82/skills/deep-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local memory files, Docker Compose configuration, and a Python memory client during setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
