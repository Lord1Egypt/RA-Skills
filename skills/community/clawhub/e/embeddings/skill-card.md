## Description:

Generate, store, and search vector embeddings with provider selection, chunking strategies, and similarity search optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose embedding providers, chunk source content, store vectors, and tune semantic search or retrieval workflows for applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted embedding and reranking examples may send supplied text to third-party providers.

Mitigation: Use local models or approved providers for sensitive data, and confirm provider data handling before submitting protected content.

Risk: Persistent vector databases can retain sensitive source text, metadata, or derived embeddings.

Mitigation: Choose storage locations deliberately, apply access controls, and avoid writing sensitive vectors to unmanaged stores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/embeddings)
- [Embedding Providers](providers.md)
- [Chunking Strategies](chunking.md)
- [Vector Storage](storage.md)
- [Search & Retrieval](search.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides provider, chunking, storage, and retrieval recommendations; does not execute tools on its own.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
