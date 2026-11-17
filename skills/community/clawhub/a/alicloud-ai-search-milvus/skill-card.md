## Description:

Use AliCloud Milvus (serverless) with PyMilvus to create collections, insert vectors, and run filtered similarity search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect agent workflows to Alibaba Cloud Milvus, create vector collections, insert records, and run filtered similarity searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Milvus database credentials and includes a plaintext HTTP endpoint pattern.

Mitigation: Prefer HTTPS/TLS endpoints, use a low-privilege Milvus account, and avoid admin tokens.

Risk: The quickstart creates a collection and inserts records.

Mitigation: Run it only against a disposable collection or test database unless the user has explicitly approved mutating operations.

Risk: Installing an unpinned PyMilvus dependency can introduce unexpected dependency changes.

Mitigation: Install PyMilvus in a virtual environment and pin the package version for repeatable use.

## Reference(s):

- [Source list](references/sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Milvus connection settings from environment variables and may save execution evidence under output/alicloud-ai-search-milvus/.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
