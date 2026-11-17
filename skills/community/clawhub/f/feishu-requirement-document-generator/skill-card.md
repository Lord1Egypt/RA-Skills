## Description:

客户需求智能整理与文档生成专家，从沟通记录、飞书文档、飞书妙记和会议纪要中提取、分析并整理结构化需求文档，并可生成飞书文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[664624249](https://clawhub.ai/user/664624249)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external delivery teams use this skill to convert Chinese customer conversations, Feishu documents, Feishu minutes, and pasted notes into structured requirements artifacts such as BRD, PRD, TRD, and SRS documents. It helps capture business context, pain points, functional and non-functional requirements, priorities, permissions, automation scenarios, views, dashboards, risks, and acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source documents may contain secrets, confidential business details, or unnecessary personal data.

Mitigation: Review and redact inputs before processing them with the agent, especially before generating or sharing a Feishu document.

Risk: Generated Feishu documents can be shared with the wrong recipient or with broader edit permissions than intended.

Mitigation: Confirm the exact recipient identity and permission level before adding document access.

Risk: Requirements extracted from meeting notes or pasted conversations may be incomplete, ambiguous, or conflicting.

Mitigation: Use the skill's confirmation checklist to mark assumptions, conflicts, missing information, and customer validation items before treating the document as final.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/664624249/skills/feishu-requirement-document-generator)
- [需求文档模板库](references/document-templates.md)
- [业务需求文档（BRD）模板](references/brd-template.md)
- [产品需求文档（PRD）模板](references/prd-template.md)
- [技术需求文档（TRD）模板](references/trd-template.md)
- [项目需求说明书（SRS）模板](references/srs-template.md)
- [高质量需求文档标准模板](references/high-quality-standard.md)
- [权限矩阵设计模板](references/permission-matrix-template.md)
- [自动化场景设计模板](references/automation-template.md)
- [视图与仪表盘设计模板](references/view-dashboard-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Chinese Markdown requirements document, optionally followed by a Feishu document link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read source documents and create, write, format, and share Feishu documents when the required Feishu tools and permissions are available.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
