## Description:

Generate images using DashScope wan2.6-t2i (通义万相 2.6) with Chinese or English prompts, custom sizes, and batch generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate PNG images from Chinese or English text prompts through Alibaba Cloud DashScope, with optional size, batch count, negative prompt, output directory, and URL-only controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to execute a local script outside the package.

Mitigation: Confirm that `~/.openclaw/scripts/dashscope-imagegen.py` exists, comes from a trusted source, and only performs the expected DashScope image-generation workflow before using the skill.

Risk: Prompts are sent to Alibaba Cloud DashScope and may contain sensitive content.

Mitigation: Avoid confidential prompts unless DashScope processing is acceptable for the intended use case.

Risk: The skill depends on `DASHSCOPE_API_KEY` for external API access.

Mitigation: Use a scoped, revocable API key and rotate or revoke it if exposure is suspected.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and setup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked workflow can download PNG image files or return image URLs when URL-only mode is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
