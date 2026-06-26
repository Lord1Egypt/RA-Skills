## Description: <br>
SDK for ingesting data into Deeplake managed tables. Use when users want to store, ingest, or query data in Deeplake. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaghni](https://clawhub.ai/user/kaghni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to help agents generate Deeplake Python and TypeScript workflows for ingesting files and structured datasets, querying managed tables, creating indexes, and opening tables for ML training or streaming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to upload local files or datasets into a Deeplake cloud workspace. <br>
Mitigation: Use a least-privileged Deeplake API key, start with a test workspace, and review the files or datasets selected for ingestion before approving the operation. <br>
Risk: Table and workspace management examples include destructive or state-changing actions such as dropping tables. <br>
Mitigation: Require explicit approval before drop_table, workspace-management, index-management, or other state-changing operations, especially in production workspaces. <br>
Risk: Raw SQL guidance can produce mutations or broad queries against managed Deeplake tables. <br>
Mitigation: Review SQL before execution, prefer parameterized queries, and apply stricter approval for any non-read query or query over sensitive datasets. <br>


## Reference(s): <br>
- [Deeplake ClawHub skill page](https://clawhub.ai/kaghni/deeplake-skills) <br>
- [Publisher profile](https://clawhub.ai/user/kaghni) <br>
- [Deeplake skills repository](https://github.com/activeloopai/deeplake-skills) <br>
- [Deeplake homepage](https://deeplake.ai) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Examples reference](artifact/examples.md) <br>
- [Formats reference](artifact/formats.md) <br>
- [SQL reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python, TypeScript, SQL, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
