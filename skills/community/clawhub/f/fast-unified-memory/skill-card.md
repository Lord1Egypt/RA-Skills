## Description: <br>
Provides a high-performance unified memory layer that combines OpenClaw file-based memory with semantic vector search using local Ollama embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add, search, list, and inspect local text memories with semantic similarity via Ollama while also searching OpenClaw memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Added memories are retained in a local store and may contain sensitive text if users add it. <br>
Mitigation: Avoid storing secrets or sensitive personal data, and review or delete ~/.mem0/fast-store.json when retained memories are no longer wanted. <br>
Risk: The installation guidance includes a curl-to-shell command for installing Ollama. <br>
Mitigation: Verify the Ollama installer before running the command. <br>
Risk: The skill depends on a local Ollama service and the nomic-embed-text model. <br>
Mitigation: Install Ollama, pull the model, and ensure the local service is running before using memory search or add commands. <br>


## Reference(s): <br>
- [Fast Unified Memory skill documentation](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/Broedkrummen/fast-unified-memory) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem memory storage and a local Ollama embedding service; no remote API key is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
