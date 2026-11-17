## Description:

Build vector retrieval with DashVector using the Python SDK. Use when creating collections, upserting docs, and running similarity search with filters in Claude Code/Codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure DashVector collections, upsert vector documents, and run filtered similarity search through the Python SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quickstart can create a collection and upsert sample documents in a DashVector cluster.

Mitigation: Run it only against a verified endpoint with a least-privileged API key and explicit collection settings.

Risk: The skill depends on API-key and endpoint configuration.

Mitigation: Keep DASHVECTOR_API_KEY scoped, rotate it as needed, and avoid exposing credentials in logs, shell history, or committed files.

Risk: An unpinned dashvector SDK install can change behavior over time.

Mitigation: Install the SDK in an isolated virtual environment and pin the package version for repeatable runs.

## Reference(s):

- [Source List](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose DashVector API calls that require DASHVECTOR_API_KEY and DASHVECTOR_ENDPOINT.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
