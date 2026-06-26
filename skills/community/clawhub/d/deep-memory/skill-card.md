## Description: <br>
One-click clone of a production-grade semantic memory system with HOT/WARM/COLD tiered storage, Qdrant vector DB, Neo4j graph DB, and qwen3-embedding for cross-session semantic retrieval and entity relationship memory for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to set up local cross-session memory with file, vector, and graph retrieval for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can start persistent local Qdrant and Neo4j database services that may store sensitive agent memories. <br>
Mitigation: Install only when persistent agent memory is intended, avoid storing secrets or highly sensitive personal data, and remove Docker volumes when the memory store is no longer needed. <br>
Risk: The Neo4j service is configured without authentication and database ports are exposed locally. <br>
Mitigation: Review the setup script before execution, enable Neo4j authentication where appropriate, and restrict Qdrant and Neo4j access to localhost or a firewall. <br>
Risk: The setup may pull a local embedding model and start Docker containers as part of installation. <br>
Mitigation: Run setup only in a trusted local environment after confirming Docker, Ollama, and container resource expectations. <br>


## Reference(s): <br>
- [Deep Memory ClawHub Page](https://clawhub.ai/halfmoon82/deep-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and usage guidance for a persistent memory stack; no API-key environment variables were detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
