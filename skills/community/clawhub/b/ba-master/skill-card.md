## Description:

BA Master Agent turns vague business or product concepts into structured requirement assets, covering requirement specifications, business process modeling, data dictionaries, user stories, UI view specifications, and compliance review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo21cn](https://clawhub.ai/user/leo21cn)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, product managers, and delivery teams use Ba Master to transform early-stage system or feature ideas into structured requirement documents, process models, data dictionaries, user stories, UI view specifications, and compliance review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User content is sent to a remote MCP service using an exposed shared bearer credential.

Mitigation: Use only data that is allowed to be sent to the configured external service; avoid confidential, regulated, customer, or credential-bearing documents unless the publisher replaces the shared token and documents data handling.

Risk: The remote MCP service can supply workflow-control instructions that influence staged interactions.

Mitigation: Constrain remote protocol behavior locally and review generated requirement or compliance assets before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leo21cn/skills/ba-master)
- [Remote MCP Service Endpoint](https://mcp.smartmoves.com.cn/ba/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown documents with tables, Mermaid diagrams, and staged human-readable prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated through staged workflows and should be reviewed before use as requirement or compliance artifacts.]

## Skill Version(s):

1.8.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
