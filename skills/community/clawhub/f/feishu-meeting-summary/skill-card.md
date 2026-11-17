## Description:

飞书会议总结技能 - 读取飞书会议纪要，生成结构化总结，沉淀知识，支持搜索

This skill is ready for commercial/non-commercial use.

## Publisher:

[yannboy](https://clawhub.ai/user/yannboy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams using Feishu use this skill to turn meeting records into detailed structured summaries, preserve source links, and save meeting knowledge into a configured Feishu knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting transcripts and generated summaries may be saved into a configured Feishu knowledge base with broader access than intended.

Mitigation: Use a least-privilege Feishu folder, review access permissions, and avoid sensitive personal, legal, financial, or confidential business material unless storage and retention are approved.

Risk: AI-generated summaries may omit details if treated as the primary meeting record.

Mitigation: Base summaries on the detailed transcript, use AI summaries only as supplemental context, and verify that original meeting links remain in the saved document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yannboy/skills/feishu-meeting-summary)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown meeting summaries, knowledge notes, and Feishu document links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the detailed meeting transcript as the primary source and AI summaries only as supplemental context.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
