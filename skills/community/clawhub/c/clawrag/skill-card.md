## Description: <br>
Self-hosted RAG connector for local document ingestion, hybrid semantic and keyword search, source citations, and OpenClaw integration through a local ClawRAG service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2dogsandanerd](https://clawhub.ai/user/2dogsandanerd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to a self-hosted ClawRAG service for local retrieval, memory, document search, and cited answers across project knowledge collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker-based setup may start local services with persistent vector data. <br>
Mitigation: Review the Docker Compose configuration before startup and confirm how to stop containers and delete stored vector data. <br>
Risk: Ingested documents may contain secrets or sensitive information. <br>
Mitigation: Avoid ingesting secrets unless necessary and prefer local-only models for sensitive documents. <br>
Risk: The release depends on an external repository and npm package. <br>
Mitigation: Install only after reviewing and trusting the referenced GitHub repository and @clawrag/mcp-server package. <br>


## Reference(s): <br>
- [ClawRAG Skill Page](https://clawhub.ai/2dogsandanerd/clawrag) <br>
- [ClawRAG Documentation](https://github.com/2dogsandanerd/ClawRag#readme) <br>
- [ClawRAG Issues](https://github.com/2dogsandanerd/ClawRag/issues) <br>
- [@clawrag/mcp-server Package](https://www.npmjs.com/package/@clawrag/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing setup and usage guidance for Docker, OpenClaw MCP configuration, and local ClawRAG service verification.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
