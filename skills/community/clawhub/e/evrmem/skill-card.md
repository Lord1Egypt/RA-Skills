## Description:

Local Chinese semantic memory search and storage using text2vec embeddings and ChromaDB, supporting RAG-based context augmentation for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhzgao](https://clawhub.ai/user/zhzgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add local Chinese semantic memory capabilities to an agent, including memory storage, search, structured queries, and RAG context retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps persistent local memories under the user's home directory.

Mitigation: Avoid storing secrets or untrusted instructions, and review retention and deletion practices before use.

Risk: The skill may install and run unpinned external Python package code and model files.

Mitigation: Use a virtual environment, review or pin the evrmem package and model source, and initialize only from trusted network locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhzgao/skills/evrmem)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and memory-addition responses use structured Markdown summaries and tables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
