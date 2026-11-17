## Description:

Analyzes, describes, and interprets images with the Qwen2.5-VL-72B vision-language model through SiliconFlow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to analyze local images or image URLs for scene description, object recognition, chart interpretation, product identification, food identification, and other visual understanding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, image URLs, and prompts are sent to SiliconFlow using the user's API key, which can create privacy exposure and token charges.

Mitigation: Use only images the user is authorized to share, avoid confidential, regulated, biometric, or proprietary content unless approved, and confirm the provider's data-handling terms and expected cost before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-vision)
- [SiliconFlow chat completions API endpoint](https://api.siliconflow.cn/v1/chat/completions)
- [SiliconFlow API key console](https://cloud.siliconflow.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with shell command examples and model-generated image analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SILICONFLOW_API_KEY; the helper script defaults to a 2048-token maximum response.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
