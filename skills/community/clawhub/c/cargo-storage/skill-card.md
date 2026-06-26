## Description: <br>
Manage models, datasets, columns, and relationships and query workspace storage with SQL using the Cargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to inspect and manage Cargo workspace storage, including models, datasets, columns, relationships, records, and SQL queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to remove models or columns and export large workspace datasets. <br>
Mitigation: Require explicit user confirmation before removal or full-export commands, preview SQL with LIMIT, and use least-privilege Cargo credentials. <br>
Risk: The install metadata references @cargo-ai/cli@latest, which can change over time. <br>
Mitigation: Review or pin the Cargo CLI package version in managed environments before granting access to production workspaces. <br>


## Reference(s): <br>
- [Cargo Storage on ClawHub](https://clawhub.ai/cargo-ai/cargo-storage) <br>
- [Cargo skills homepage](https://github.com/getcargohq/cargo-skills) <br>
- [Response shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Model examples](references/examples/models.md) <br>
- [Dataset examples](references/examples/datasets.md) <br>
- [Column examples](references/examples/columns.md) <br>
- [Storage query examples](references/examples/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require @cargo-ai/cli and Cargo authentication.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
