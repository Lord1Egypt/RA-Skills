## Description:

Local-first memory retrieval for Agent/OpenClaw workspaces that searches Markdown memory files and returns explainable matches for prior decisions, incidents, preferences, and change history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to answer memory questions from local Markdown notes, inspect why results matched, rebuild a local index, and debug retrieval quality without depending on a hosted memory platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local index stores plaintext snippets from MEMORY.md and memory/*.md in the workspace.

Mitigation: Do not index secrets or confidential notes; review memory files before indexing and protect or remove the generated .memory-index directory according to the workspace data policy.

Risk: Optional SiliconFlow reranking can send selected local memory excerpts to an external API when an API key is present.

Mitigation: Set MEMORY_RERANK=0 for local-only operation and avoid exposing a generic API_KEY in the runtime environment unless external reranking is intended.

## Reference(s):

- [Architecture](artifact/references/architecture.md)
- [Regression Queries](artifact/references/regression-queries.md)
- [Regression Cases](artifact/references/regression-cases.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON retrieval results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval results include source file, title, snippet, scores, anchor hits, overlap terms, index status, and optional rerank metadata.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
