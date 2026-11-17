## Description:

Generate images via Alibaba DashScope OpenAI-compatible endpoint (compatible-mode) using qwen-image-max.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhdragon](https://clawhub.ai/user/dhdragon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate image files from text prompts through Alibaba DashScope compatible-mode, including scriptable CLI workflows against an OpenAI-style /images/generations endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse a local OpenClaw DashScope API key and send it to a caller-selected endpoint.

Mitigation: Prefer explicit DASHSCOPE_API_KEY use, avoid custom --base-url values, and require endpoint allowlisting before using paid API credentials.

Risk: The skill downloads image content returned by the image generation service.

Mitigation: Use bounded output paths and review generated files before trusting or redistributing them.

## Reference(s):

- [DashScope OpenAI Compatible-mode notes](references/dashscope-openai-compatible.md)
- [DashScope compatible-mode endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples; the helper script writes generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a text prompt plus optional size, image count, seed, model, API key, base URL, and output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
