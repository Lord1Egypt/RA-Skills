## Description:

为课程媒体转写或校对 SRT/VTT 字幕，供用户逐项确认后导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

课程教师和内容制作人员可用此技能转写课程媒体，或校对现有 SRT/VTT 字幕；用户逐项确认建议后可导出字幕和复核报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Course media and subtitle content may be sent to configured speech or text providers and retained for 30 days.

Mitigation: Explain the transfer scope and retention before processing, and handle only materials the user is authorized to upload.

Risk: Transcription and model proofreading may incur usage charges.

Mitigation: Show current pricing and frozen task details, obtain approval before paid work, and check the original task when its outcome is unknown.

Risk: Suggested subtitle edits may be incorrect or out of context.

Mitigation: Present suggestions individually and treat a revision as confirmed only after the user explicitly reviews it.

## Reference(s):

- [AI Skills 平台](https://ai-skills.open-idea.net)
- [平台密钥与费用](https://ai-skills.open-idea.net/skill-docs/course-subtitle/API-KEY.md)
- [上传、请求与轮询](https://ai-skills.open-idea.net/skill-docs/course-subtitle/HTTP-REQUESTS.md)
- [操作字段与最小流程](https://ai-skills.open-idea.net/skill-docs/course-subtitle/OPERATIONS.md)
- [授权、隐私与人工确认](https://ai-skills.open-idea.net/skill-docs/course-subtitle/BEHAVIOR-RULES.md)
- [ClawHub 技能页面](https://clawhub.ai/youteacher/skills/course-subtitle)

## Skill Output:

**Output Type(s):** [Subtitle files, JSON report, Guidance]

**Output Format:** [SRT, VTT, JSON review report, and task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private exports; unresolved suggestions remain drafts until the user reviews them.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
