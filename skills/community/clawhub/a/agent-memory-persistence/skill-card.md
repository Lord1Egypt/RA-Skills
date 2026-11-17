## Description:

Provide long-term memory persistence for AI agents with SQLite-backed storage, structured metadata, vector embeddings, semantic retrieval, lifecycle management, and queries by user, session, and time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgolye](https://clawhub.ai/user/imgolye)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add durable local memory across sessions, including structured metadata, vector embeddings, semantic lookup, and lifecycle cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can retain secrets, sensitive conversation content, or stale personal data if agents write it unfiltered.

Mitigation: Avoid storing secrets or highly sensitive content unless the database path, file permissions, retention policy, and deletion workflow are controlled.

Risk: Dependency ranges are not pinned exactly, which can reduce reproducibility and supply-chain control.

Mitigation: Pin dependencies or use a lockfile and trusted install workflow for stricter deployments.

Risk: Vector search uses full scans with cosine similarity, which may not scale to large memory stores.

Mitigation: For large stores, replace VectorIndex with an ANN index or SQLite vector extension while preserving the MemoryManager API.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite-backed memory operations for agents; no network behavior was identified in the server security evidence.]

## Skill Version(s):

0.1.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
