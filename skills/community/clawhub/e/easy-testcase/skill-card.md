## Description:

将需求文档、表单字段规则、审批流程定义和 UI 说明转化为结构化测试用例，适用于表单校验、流程审批、状态流转、权限隔离和业务分支测试场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lens-lzy](https://clawhub.ai/user/lens-lzy)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, product teams, and developers use this skill to turn PRDs, field rules, workflow definitions, UI notes, and related requirements into executable test cases. It is especially suited for form validation, approval flow, state transition, permission, and business-branch testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated test cases can be incomplete or misleading when the supplied requirements are incomplete, ambiguous, or conflicting.

Mitigation: Review the Markdown test cases against the source requirements and use the generated clarification questions to resolve gaps before execution.

Risk: Requested Feishu, drive, or local-file output may not be available in every agent environment.

Mitigation: Confirm the target tool and destination are available before requesting document creation, upload, or file writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lens-lzy/skills/easy-testcase)
- [Publisher profile](https://clawhub.ai/user/lens-lzy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with an optional Markdown requirements-clarification section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese-language output; optional Feishu document, drive upload, or local file output depends on available tools and explicit user request.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
