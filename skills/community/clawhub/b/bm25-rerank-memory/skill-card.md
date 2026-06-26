## Description: <br>
Provides local hybrid memory retrieval with BM25 keyword search, BGE-M3 embeddings, and BGE reranking over Markdown memory files under /root/workspace/Remember. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckqiao](https://clawhub.ai/user/ckqiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search local Markdown memory files and retrieve ranked context snippets for a query. It is intended to replace mem0 for memory search workflows that need hybrid keyword, semantic, and reranked results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run /opt/memory/bm25_rerank_search.py, which is not included in the artifact and cannot be reviewed from this release package. <br>
Mitigation: Review the local script before installation or execution and run it only in an environment where its behavior is trusted. <br>
Risk: Memory search may send private memory content to SiliconFlow for embedding and reranking. <br>
Mitigation: Avoid using the skill on sensitive memories unless data handling with SiliconFlow is understood and acceptable. <br>
Risk: The documented dependency command modifies the system Python environment with --break-system-packages. <br>
Mitigation: Install dependencies in an isolated environment with pinned versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckqiao/bm25-rerank-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and ranked text result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include score, path, chunk_id, and a content snippet capped at 200 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
