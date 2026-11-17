## Description:

Provides semantic vector search over Aister memory files using PostgreSQL, pgvector, and e5-large-v2 embeddings for Russian and English content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alekhm](https://clawhub.ai/user/alekhm)

### License/Terms of Use:

MIT License

## Use Case:

Developers and Aister users use this skill to index local memory files and retrieve related context by semantic similarity instead of keyword matching. It supports memory search and reindexing workflows backed by a local PostgreSQL vector database and embedding service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private memory files are indexed into PostgreSQL and may include sensitive personal, credential, or operational content.

Mitigation: Review memory files before indexing, run the database in an isolated environment, and use a dedicated database user with minimal required privileges.

Risk: Memory chunks and search queries can be sent to a configurable embedding service URL.

Mitigation: Keep EMBEDDING_SERVICE_URL bound to 127.0.0.1 unless a remote service is explicitly trusted to receive that content.

Risk: Optional autostart can keep the embedding service running after setup.

Mitigation: Enable autostart only after reviewing how the service is launched, stopped, logged, and updated in the target environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/alekhm/skills/aister-vector-memory)
- [Publisher profile](https://clawhub.ai/user/alekhm)
- [Artifact README](artifact/README.md)
- [Installation guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus text or JSON search results from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes source metadata and similarity scores when results are returned.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
