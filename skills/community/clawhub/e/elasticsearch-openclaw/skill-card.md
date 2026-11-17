## Description:

Read-only Elasticsearch 9.x reference for AI-orchestrated search and analytics, covering semantic search, vector search, hybrid retrieval, classic query patterns, Python client 9.x usage, and least-privilege API-key guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salgado](https://clawhub.ai/user/salgado)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose and draft Elasticsearch 9.x read-only search, aggregation, semantic, vector, and hybrid retrieval patterns for agent-assisted applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is documentation-only and service-focused, but its examples include copyable Elasticsearch write and administrator setup operations.

Mitigation: Review examples before use, and run index creation, ingestion, inference endpoint setup, pipeline creation, API-key creation, and cluster-setting changes only as separate administrator tasks outside the normal agent environment.

Risk: The skill requires external Elasticsearch credentials and may use JINA credentials for embedding workflows.

Mitigation: Use only narrowly scoped read-only Elasticsearch API keys in the agent workspace, keep secrets in environment files, and do not broaden credentials to make setup examples work.

## Reference(s):

- [Classic Patterns - Updated for ES 9.x](references/classic-patterns.md)
- [Elasticsearch Python Client 9.x](references/python-client-9.md)
- [Semantic Search - JINA and semantic_text](references/semantic-search.md)
- [Vector Search - kNN, dense_vector, Hybrid Search](references/vector-search.md)
- [Elastic start-local repository](https://github.com/elastic/start-local)
- [Elastic start-local documentation](https://www.elastic.co/start-local)
- [Jina embeddings](https://jina.ai/embeddings)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only reference material for read-only Elasticsearch usage; requires external Elasticsearch credentials and may reference optional JINA credentials.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
