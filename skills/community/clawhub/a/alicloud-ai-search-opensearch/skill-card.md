## Description:

Use OpenSearch vector search edition via the Python SDK (ha3engine) to push documents and run HA/SQL searches for RAG and vector retrieval pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Alibaba Cloud OpenSearch vector search workflows, push documents, and run HA or SQL-style searches. It is suited to RAG and vector retrieval pipelines that need SDK-oriented guidance and quickstart commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quickstart configures the OpenSearch SDK with plaintext HTTP while using username and password credentials.

Mitigation: Change the SDK configuration to HTTPS before use and avoid sending credentials over plaintext connections.

Risk: The quickstart performs mutating document push operations.

Mitigation: Run a minimal read-only query first, use least-privilege credentials, and avoid production data until writes are explicitly approved.

Risk: The SDK dependency is installed directly in setup examples without a reviewed pinned requirements file.

Mitigation: Pin the SDK dependency in a reviewed requirements file before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-search-opensearch)
- [Artifact source list](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks, configuration notes, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to produce command outputs and API response summaries under output/alicloud-ai-search-opensearch/.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
