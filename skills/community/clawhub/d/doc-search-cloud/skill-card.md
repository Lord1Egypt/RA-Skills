## Description:

Doc Search vectorizes Word, Markdown, PDF, and text documents, stores document chunks locally, and supports semantic and hybrid BM25/vector retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcba](https://clawhub.ai/user/cloudcba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build local document retrieval workflows that ingest files, create embeddings, and return relevant text chunks for a query. It is intended for document search and vector-store management rather than conversational memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local persistence can retain sensitive document content in the vector store.

Mitigation: Use only a trusted local persistence directory and avoid indexing sensitive documents unless local retention is acceptable.

Risk: Pickle-based loading can execute attacker-controlled code if persisted storage files are tampered with.

Mitigation: Do not open vector stores from other people; ask the publisher to replace pickle storage with a safer serialization format.

Risk: Optional model loading may pull in additional dependency and model behavior that reviewers have not approved.

Mitigation: Use a pinned dependency setup and keep real embedding model loading behind explicit user choice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudcba/skills/doc-search-cloud)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and structured JSON-like result shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local vector-store files and retrieval results containing indexed document text.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; artifact frontmatter states v3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
