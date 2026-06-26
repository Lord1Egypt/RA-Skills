## Description: <br>
Local vector memory system for agent recall using LanceDB and JavaScript embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LHMiles](https://clawhub.ai/user/LHMiles) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to initialize, store, search, and manage durable local memories for an OpenClaw-style agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports under-disclosed remote API and shell-download code paths that do not fit the skill's local-only claims. <br>
Mitigation: Review or remove the unused Kimi and ONNX embedding helpers before installing in sensitive environments. <br>
Risk: Stored memories are durable local records and may retain sensitive user or project information. <br>
Mitigation: Avoid storing secrets or regulated data, review memory contents regularly, and disable autoRecall if automatic injection of prior memories is not wanted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/LHMiles/elite-longterm-memory-local) <br>
- [Ollama](https://ollama.com) <br>
- [LanceDB Documentation](https://lancedb.github.io) <br>
- [nomic-embed-text Model](https://ollama.com/library/nomic-embed-text) <br>
- [Kimi API](https://api.kimi.com/coding) <br>
- [Xenova all-MiniLM-L6-v2 Model Mirror](https://hf-mirror.com/Xenova/all-MiniLM-L6-v2/resolve/main) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local memory files and vector-store data in the user's workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
