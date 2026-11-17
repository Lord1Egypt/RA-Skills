## Description:

帮助投标人员解读招标文件、生成投标文件，并审查合规性及多份标书的相似风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

投标人员和采购团队可上传招标或投标文件，获取招标要求解读、投标文件草稿、合规审查及标书查重结果。文件由第三方云服务处理，部分操作按可用字数计费。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents are sent to a third-party cloud service for processing.

Mitigation: Confirm authorization and confidentiality requirements before uploading sensitive documents.

Risk: Automatic trial enrollment collects device characteristics despite incomplete disclosure in the skill's permissions summary.

Mitigation: Avoid the trial unless the user consents to device fingerprinting; use a separately obtained API key instead.

Risk: Saved API keys and keys pasted into chat can expose paid account access.

Mitigation: Use a dedicated, revocable key; keep it out of chat and links, and restrict access to saved credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liu-jiapeng/skills/biaoshu-writer-transit)
- [百炼标书服务](https://biaoshu.zhiliaobiaoxun.com/)
- [API overview](references/api.md)
- [Usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Conversational summaries, HTML or Word reports, and DOCX bid documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents may be delivered by short-lived download link; review all bid content before submission.]

## Skill Version(s):

2.0.6 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
