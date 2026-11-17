## Description:

Use when building vector retrieval with DashVector using the Python SDK, including collection creation, document upserts, and filtered similarity search in Claude Code or Codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Alibaba Cloud DashVector access, create collections, ingest vectors, and run bounded similarity searches with optional filters. It is intended for retrieval workflows that need repeatable Python SDK examples and operational checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quickstart requires a DashVector API key and endpoint, which could expose or misuse cloud resources if configured broadly or incorrectly.

Mitigation: Use a narrowly scoped DashVector API key, keep credentials in environment variables, and verify DASHVECTOR_ENDPOINT against the Alibaba Cloud DashVector console before running operations.

Risk: The bundled quickstart creates a collection and upserts documents, so running it against a production collection could mutate live data.

Mitigation: Run mutating quickstart operations only against a test collection or an explicitly selected collection after confirming user intent, region, identifiers, and scope.

Risk: Vector dimensions, filters, or collection schemas that do not match the embedding workflow can cause failed requests or misleading retrieval results.

Mitigation: Keep collection dimensions aligned to the embedding model output size, validate schema and filters with a minimal read-only query first, and save response summaries for review.

## Reference(s):

- [Source list](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-dashvector-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DashVector collection names, vector dimensions, filters, environment variable names, and API response summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
