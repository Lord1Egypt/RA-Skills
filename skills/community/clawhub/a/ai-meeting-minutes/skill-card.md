## Description:

AI 会议纪要生成器 - 自动整理会议录音或文字记录，生成结构化会议纪要。支持提取待办事项、决策点、关键结论，输出专业格式的会议文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and agents use this skill to turn meeting transcripts or recordings into structured minutes with summaries, decisions, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting audio and transcripts can contain sensitive personal, business, or regulated information.

Mitigation: Confirm participant consent, follow organizational policy for API-based processing, and avoid highly confidential content unless approved.

Risk: Generated minutes may be saved to files and retained after the meeting workflow completes.

Mitigation: Review generated minutes for sensitive content and delete or store output according to retention policy.

Risk: The artifact references scripts/minutes.mjs, but that implementation is not included in the supplied artifact.

Mitigation: Verify the required script is supplied elsewhere before relying on the skill for execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/skills/ai-meeting-minutes)
- [Publisher profile](https://clawhub.ai/user/ryan-wuxl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can summarize transcripts or recordings into meeting minutes, decisions, and action items; generated minutes may be saved to files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
