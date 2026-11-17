## Description:

基于 AnyShare 的专家写作助手 - 上传项目文件到文档库，调用全文写作技能生成大纲文档，确认后基于大纲生成正文

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyshare-aishu](https://clawhub.ai/user/anyshare-aishu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to turn uploaded project materials into professional Chinese business, project, report, and solution documents through a two-stage outline then body workflow. It is suited for AnyShare-based writing workflows where the user can review the outline before final generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can upload user documents to AnyShare and use them as source material.

Mitigation: Use only documents approved for AnyShare processing, confirm the target document library before upload, and avoid confidential materials unless the deployment has been reviewed.

Risk: Generated body content or sharing can proceed after inactivity or without a fresh explicit confirmation.

Mitigation: Require an explicit current user confirmation before final body generation or share-link creation, and disable timeout auto-proceed for sensitive workflows.

Risk: Access tokens and temporary files are part of the workflow and could expose sensitive access or content if mishandled.

Mitigation: Use a least-privilege token stored in the configured mcporter location, avoid logging credentials, and clean temporary outline and selection files after use.

Risk: Generated share links may expose output documents beyond the intended audience.

Mitigation: Verify share-link recipients, permissions, and expiry before distributing any generated link.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anyshare-aishu/skills/expert-writing-asmcp)
- [Publisher Profile](https://clawhub.ai/user/anyshare-aishu)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Template Index](templates/README.md)
- [AnyShare ASMCP Service](https://anyshare.aishu.cn/asmcp/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documents with supporting shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces outline and body drafts from uploaded reference documents, and may save generated documents and share links in AnyShare.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
