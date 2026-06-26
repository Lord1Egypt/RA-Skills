## Description: <br>
Builds ByteHouse hybrid search workflows that combine BM25 full-text search, HNSW vector search, and Reciprocal Rank Fusion reranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to configure ByteHouse-backed retrieval over document tables, generate embeddings with the Ark API, and run full-text, vector, or hybrid searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses ByteHouse credentials and can create tables or insert and update documents. <br>
Mitigation: Use least-privilege database credentials and require confirmation before table creation, inserts, or updates. <br>
Risk: Document text may be sent to the configured Ark embedding endpoint for vector generation. <br>
Mitigation: Verify the endpoint and avoid sending confidential or regulated text unless policy and data handling requirements allow it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-bytehouse-hybrid-search) <br>
- [ByteHouse full-text search documentation](https://www.volcengine.com/docs/6464/1208708) <br>
- [ByteHouse vector search documentation](https://www.volcengine.com/docs/6464/1208707) <br>
- [Reciprocal Rank Fusion paper](https://plg.uwaterloo.ca/~gvcormac/cormackpapers/trec03cormack.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database table creation, document writes, embedding generation, and retrieval queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
