## Description:

使用 CogVideoX (智谱AI) 模型根据文本提示词生成视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilaus](https://clawhub.ai/user/ilaus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit text prompts to CogVideoX through Zhipu AI and receive video generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full prompts may be logged, which can expose private or confidential prompt content.

Mitigation: Avoid sending sensitive prompts unless logging is removed or redacted before use.

Risk: Raw provider details may be returned to the agent or user.

Mitigation: Return only sanitized status, message, and video URL fields in production workflows.

Risk: Polling can continue indefinitely, which can affect availability, API quota, or cost controls.

Mitigation: Add a bounded timeout, retry limit, and clear failure response before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilaus/skills/cogvideox-generator)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [JSON-like status object with message, video URL when successful, and error details when unavailable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPUAI_API_KEY and supports prompt, quality, size, fps, and audio options.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
