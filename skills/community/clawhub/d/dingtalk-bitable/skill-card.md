## Description:

Integrates with DingTalk Bitable APIs so an agent can manage tables, inspect fields, and create, read, update, or delete records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxwos](https://clawhub.ai/user/cxwos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent work with DingTalk Bitable workspaces, including table discovery, field inspection, record queries, and controlled record or schema changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, and delete live DingTalk Bitable records.

Mitigation: Require human confirmation before mutation requests and review target app, table, and record identifiers before execution.

Risk: The skill uses local DingTalk app credentials to access remote workspace data.

Mitigation: Use least-privilege DingTalk app credentials and avoid broad workspace permissions.

## Reference(s):

- [DingTalk Tables Overview](https://open.dingtalk.com/document/orgapp/overview-of-dingtalk-tables)
- [DingTalk Open Platform API Reference](https://open.dingtalk.com/document/orgapp)
- [ClawHub Skill Page](https://clawhub.ai/cxwos/skills/dingtalk-bitable)
- [Publisher Profile](https://clawhub.ai/user/cxwos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples and JSON-shaped tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DingTalk credentials and the Python requests package.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
