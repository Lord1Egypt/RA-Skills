## Description:

Long-term memory via ChromaDB with local Ollama embeddings. Auto-recall injects relevant context every turn. No cloud APIs required; fully self-hosted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msensintaffar](https://clawhub.ai/user/msensintaffar)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to connect an OpenClaw agent to a ChromaDB collection and local Ollama embedding model for long-term memory recall. It supports automatic context injection before turns and manual semantic search with the `chromadb_search` tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-recall can reuse broad or under-scoped stored memory in every turn, including prompt-injection content from the ChromaDB collection.

Mitigation: Disable autoRecall until the collection is configured and trusted, isolate collections per user or project, avoid storing secrets, and tune minScore and result limits.

Risk: Untrusted ChromaDB collections, OpenClaw plugin configuration, or Ollama and Chroma endpoints can influence agent context and outputs.

Mitigation: Install only when those inputs are trusted, keep endpoints local or explicitly trusted, and pin the ChromaDB image version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/msensintaffar/skills/chromadb-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepend retrieved ChromaDB memory snippets or ChromaDB availability warnings to an agent turn when auto-recall is enabled.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter and manifest list 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
