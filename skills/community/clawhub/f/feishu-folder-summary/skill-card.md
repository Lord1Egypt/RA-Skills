## Description:

Extracts and summarizes documents from a Feishu wiki space or drive folder into a structured Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryjing96](https://clawhub.ai/user/henryjing96)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to recursively inspect Feishu wiki or drive folders they can access and produce a readable summary report with document links, status, statistics, and a directory tree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recursively read and summarize many Feishu documents, including confidential or regulated workspace content.

Mitigation: Confirm the exact folder URL, expected document count, recursion depth, and output destination before document reads begin.

Risk: Generated Markdown may include document titles or content supplied by other Feishu users.

Mitigation: Treat the report as untrusted content and review it before sharing, publishing, or using links and titles operationally.

## Reference(s):

- [Feishu API Reference](references/feishu_api.md)
- [ClawHub skill page](https://clawhub.ai/henryjing96/skills/feishu-folder-summary)

## Skill Output:

**Output Type(s):** [Markdown, Text, API Calls]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a directory tree, hierarchical summaries, document status counts, statistics, generation metadata, and source document links.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
