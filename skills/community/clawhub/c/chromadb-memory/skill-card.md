## Description: <br>
Long-term memory via ChromaDB with local Ollama embeddings. Auto-recall injects relevant context every turn. No cloud APIs required; fully self-hosted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msensintaffar](https://clawhub.ai/user/msensintaffar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve long-term semantic memory from a configured ChromaDB collection and inject relevant context into agent turns. It supports both automatic recall and manual ChromaDB search for historical context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic recall may add sensitive or unintended memories from the configured ChromaDB collection into agent context. <br>
Mitigation: Avoid indexing secrets or sensitive documents, review collection contents, and set autoRecall to false when manual search is preferred. <br>
Risk: Memory retrieval depends on ChromaDB and Ollama endpoints being reachable and trusted. <br>
Mitigation: Run ChromaDB and Ollama locally or on a trusted private network and monitor surfaced availability warnings. <br>
Risk: Using a floating ChromaDB container tag can introduce unreviewed server changes. <br>
Mitigation: Pin the ChromaDB Docker image version before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/msensintaffar/chromadb-memory) <br>
- [README.md](artifact/README.md) <br>
- [OpenClaw plugin metadata](artifact/scripts/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown context snippets returned to the agent, plus JSON configuration fields for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manual search returns ranked text snippets; auto-recall can prepend matching ChromaDB memories or availability warnings to the agent context.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
