## Description:

Searches local Markdown memory files under /root/workspace/Remember using BM25 keyword retrieval, BGE-M3 embeddings, and BGE reranking as a replacement for mem0 memory search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckqiao](https://clawhub.ai/user/ckqiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve concise memory snippets from local Markdown notes and rebuild the retrieval index after memory files change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve broad local memory content that may include private conversations, credentials, business data, or internal instructions.

Mitigation: Run it only in an environment where the indexed memory directory is intentionally scoped and reviewed for sensitive content.

Risk: Embedding and reranking route memory content through the external SiliconFlow processing path.

Mitigation: Use the skill only when that external processing path is trusted for the data being searched.

Risk: The skill relies on the local /opt/memory/bm25_rerank_search.py script and a dependency installation command.

Mitigation: Review the local script before installation or use, pin dependencies, and prefer an isolated runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckqiao/skills/bm25-rerank-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and text result snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include score, path, chunk identifier, and a content snippet of up to 200 characters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
