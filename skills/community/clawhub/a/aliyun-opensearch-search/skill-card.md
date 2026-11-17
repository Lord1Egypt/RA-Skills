## Description:

Use when working with OpenSearch vector search edition via the Python SDK (ha3engine) to push documents and run HA/SQL searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Alibaba Cloud OpenSearch vector search access, push sample documents, and run HA or SQL-style searches for RAG and vector retrieval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quickstart uses OpenSearch credentials and a plaintext HTTP client setting.

Mitigation: Review or change the client configuration to use HTTPS and run only with narrowly scoped credentials.

Risk: The quickstart can write sample documents to a live OpenSearch datasource.

Mitigation: Run the quickstart against a test or disposable datasource before using it with production resources.

Risk: The SDK dependency is not pinned in the skill instructions.

Mitigation: Pin and review the alibabacloud-ha3engine package version before relying on the workflow in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-opensearch-search)
- [Source list](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment-variable setup, quickstart commands, API usage snippets, validation steps, and risk-aware execution guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
