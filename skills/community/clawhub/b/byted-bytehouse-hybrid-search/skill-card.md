## Description:

This skill helps agents build and use ByteHouse hybrid search with BM25 full-text retrieval, HNSW vector retrieval, and Reciprocal Rank Fusion reranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure ByteHouse tables for hybrid retrieval, generate embeddings, insert or update document vectors, and combine full-text and vector results through RRF reranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ByteHouse credentials and constructs SQL with caller-provided table names and limits.

Mitigation: Use a least-privileged ByteHouse account, validate table names and limits before use, and review generated SQL before production execution.

Risk: Document and query text may be sent to a configurable embedding service.

Mitigation: Restrict ARK_BASE_URL to the intended HTTPS provider and avoid sending confidential or regulated text unless policy permits it.

Risk: Runtime dependencies and external database or embedding services affect production behavior.

Mitigation: Pin and review dependencies, configure secrets through environment variables, and test against a non-production ByteHouse database before deployment.

## Reference(s):

- [Byted Bytehouse Hybrid Search on ClawHub](https://clawhub.ai/volcengine-skills/skills/byted-bytehouse-hybrid-search)
- [ByteHouse Full-Text Search Documentation](https://www.volcengine.com/docs/6464/1208708)
- [ByteHouse Vector Search Documentation](https://www.volcengine.com/docs/6464/1208707)
- [Reciprocal Rank Fusion Paper](https://plg.uwaterloo.ca/~gvcormac/cormackpapers/trec03cormack.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, SQL, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable examples, environment-variable configuration, SQL statements, and retrieval result structures.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
