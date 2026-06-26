## Description: <br>
Local Chinese semantic memory search and storage using text2vec embeddings and ChromaDB, supporting RAG-based context augmentation for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhzgao](https://clawhub.ai/user/zhzgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to save, search, query, and retrieve local semantic memories for Chinese-language knowledge recall and RAG context augmentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install an external Python package and download an embedding model. <br>
Mitigation: Install only from trusted package and model sources, approve installation and initialization steps explicitly, and prefer a virtual environment. <br>
Risk: Saved memories are stored on disk and may later influence agent answers. <br>
Mitigation: Do not store secrets, credentials, regulated personal data, or untrusted instructions in memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhzgao/evrmem) <br>
- [Publisher profile](https://clawhub.ai/user/zhzgao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, shell, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results and memory additions are presented as structured Markdown.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
