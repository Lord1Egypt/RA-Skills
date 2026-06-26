## Description: <br>
Generate, store, and search vector embeddings with provider selection, chunking strategies, and similarity search optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to choose embedding providers, chunk source content, store vectors, and tune semantic retrieval workflows for applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents, code, queries, and metadata may be sent to third-party embedding or reranking services. <br>
Mitigation: Use local models for confidential or regulated data, and review provider data handling before sending sensitive content. <br>
Risk: Vector stores can retain embedded sensitive content and associated metadata. <br>
Mitigation: Apply retention, access control, and deletion policies to vector databases created from sensitive material. <br>
Risk: API keys used for embedding providers or managed vector databases could be exposed during integration. <br>
Mitigation: Protect credentials with environment secrets or a managed secret store, and avoid hard-coding keys in generated examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/embeddings) <br>
- [Embedding Providers](artifact/providers.md) <br>
- [Chunking Strategies](artifact/chunking.md) <br>
- [Vector Storage](artifact/storage.md) <br>
- [Search & Retrieval](artifact/search.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration instructions] <br>
**Output Format:** [Markdown with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider recommendations, chunking plans, vector database patterns, and retrieval tuning advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
