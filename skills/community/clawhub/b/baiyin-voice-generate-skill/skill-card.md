## Description:

使用百音开放平台创建 AI 语音任务，支持文本转语音、音色克隆，并在同一 skill 内继续查询任务状态和结果链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create Baiyin AI voice generation tasks, clone or select a voice, check task progress, and retrieve generated audio links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a silent remote self-update before normal use.

Mitigation: Remove the silent self-update behavior, or move updates to a trusted package manager flow that requires explicit approval and signed, pinned releases.

## Reference(s):

- [Baiyin Open Platform API endpoint](https://ai.hikoon.com)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [Markdown text with JSON request examples and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIYIN_API_KEY and uses Baiyin voice task IDs, model codes, public voice URLs, speed, pitch, and emotion parameters.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
