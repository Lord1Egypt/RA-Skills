## Description:

根据栏目、样例与本期素材，生成带来源核验和人工校订清单的可编辑企业期刊底稿，并提供版面与编辑质量检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

企业编辑与传播团队可用它为内刊、客户通讯、投资者信或 ESG 特刊整理素材、核对引证并生成可编辑底稿。发布前仍需人工完成编辑、事实和合规审阅。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports remote-service discovery and credential transmission beyond the stated drafting purpose.

Mitigation: Review the service and API-key instructions before use; provide CUE_API_KEY only when choosing the related service, and keep it out of drafts and shared materials.

Risk: External document processing may expose sensitive publication materials.

Mitigation: Obtain explicit approval before uploading internal documents, and confirm that the selected processing service is acceptable for those materials.

Risk: Optional skill-generation and image capabilities may exceed the task's needs.

Mitigation: Decide whether these capabilities are needed before enabling them, and review generated content before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-journal-draft)
- [Cue API key](https://cuecue.cn/hub/api-key)
- [Cue](https://cuecue.cn)
- [Content sourcing guidance](artifact/references/content-sourcing.md)
- [Editorial QA checklist](artifact/references/qa-checklist.md)
- [Editable output guidance](artifact/references/editable-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Shell commands, Files]

**Output Format:** [Markdown, HTML, PDF, DOCX, JSON, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft materials include source links and review checklists; human review is required before publication.]

## Skill Version(s):

0.15.28 (source: server-resolved ClawHub release metadata; artifact frontmatter agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
