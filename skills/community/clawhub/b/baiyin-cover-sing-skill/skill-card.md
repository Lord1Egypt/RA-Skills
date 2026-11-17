## Description:

当用户希望通过百音开放平台创建 AI 歌手翻唱任务、查询翻唱任务状态，或根据已有 taskId 返回最终翻唱音频结果时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create Baiyin AI singer cover tasks, check task status, and retrieve completed cover audio results. It guides model selection, request parameters, file upload needs, polling, and result handling for the Baiyin Open Platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a silent remote self-update before normal use, which can change behavior outside the user's immediate review.

Mitigation: Review before installing and prefer a version where updates are platform-managed, verified, and explicitly approved.

Risk: The skill uses a Baiyin API key and may upload user-provided audio to the Baiyin Open Platform.

Mitigation: Use a scoped API key where available and confirm the user is permitted to upload the audio before creating or uploading task inputs.

## Reference(s):

- [Baiyin Open Platform](https://ai.hikoon.com)
- [ClawHub skill page](https://clawhub.ai/jiuping520/skills/baiyin-cover-sing-skill)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown with API request details and result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task identifiers, status values, audio URLs, upload guidance, and error explanations.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
