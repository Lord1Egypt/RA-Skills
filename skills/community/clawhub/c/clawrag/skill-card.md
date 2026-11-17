## Description:

ClawRAG connects an agent to a self-hosted RAG and memory system with document ingestion, hybrid semantic and keyword search, source citations, and local deployment through Docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2dogsandanerd](https://clawhub.ai/user/2dogsandanerd)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to deploy a local ClawRAG service and connect it to OpenClaw through an MCP server for private document search and retrieval-augmented memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path uses mutable Docker and npm dependencies that can execute changed third-party code.

Mitigation: Review before installing, pin repository commits, container image digests, and the exact @clawrag/mcp-server version, and inspect Docker Compose, Dockerfiles, mounts, ports, and environment handling.

Risk: Local containers and the MCP process may access files, ports, or credentials beyond what the workflow needs.

Mitigation: Run with limited privileges and avoid exposing unrelated API keys or private files to containers or the MCP process.

## Reference(s):

- [ClawRAG ClawHub Page](https://clawhub.ai/2dogsandanerd/skills/clawrag)
- [ClawRAG Documentation](https://github.com/2dogsandanerd/ClawRag#readme)
- [@clawrag/mcp-server Package](https://www.npmjs.com/package/@clawrag/mcp-server)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup, verification, and connection steps for a local Docker and MCP deployment.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
