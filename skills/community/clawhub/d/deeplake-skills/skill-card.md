## Description:

SDK for ingesting data into Deeplake managed tables for storing, ingesting, and querying Deeplake data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaghni](https://clawhub.ai/user/kaghni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent install and apply Deeplake Python or TypeScript SDK workflows for ingesting local files, structured data, embeddings, and domain datasets, then querying or managing Deeplake tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use a Deeplake API key to read selected local files and upload data or derived artifacts.

Mitigation: Use a narrowly scoped token and require explicit confirmation before uploading sensitive data.

Risk: The skill includes table deletion actions through drop_table and dropTable.

Mitigation: Require explicit confirmation before any destructive table-management action.

Risk: The skill permits configured API endpoints, including plaintext HTTP endpoints for local development.

Mitigation: Use HTTPS endpoints except for trusted local development environments.

Risk: Unpinned package installation may change behavior over time.

Mitigation: Pin dependencies where possible before using the skill in controlled environments.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/kaghni/skills/deeplake-skills)
- [Deeplake Skills Repository](https://github.com/activeloopai/deeplake-skills)
- [Deeplake](https://deeplake.ai)
- [Reference Guide](artifact/reference.md)
- [Examples](artifact/examples.md)
- [Format Classes](artifact/formats.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Python, TypeScript, and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API usage guidance requiring DEEPLAKE_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
