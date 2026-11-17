## Description:

China Image Gen helps agents generate text-to-image outputs in China through the SiliconFlow API, including FLUX.1, Kolors, and SD3 model options without VPN access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to choose a SiliconFlow image model, prepare prompts and parameters, call the image-generation API, and return the resulting image URL with reproducible settings.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Image prompts are sent to SiliconFlow as a third-party provider.

Mitigation: Treat prompts as third-party data and avoid secrets, personal identifiers, confidential work, or regulated data.

Risk: The skill requires a user-provided SiliconFlow API key.

Mitigation: Keep SILICONFLOW_API_KEY private, avoid committing it to files, and rotate it if exposed.

Risk: Generated image URLs may be temporary and can expire after a short period.

Mitigation: Download needed images promptly and keep the prompt, seed, model, and parameter details for reproducibility.

Risk: Provider policy or prompt validation can reject prohibited image requests.

Mitigation: Revise prompts to comply with the provider's safety restrictions and avoid prohibited content categories.

## Reference(s):

- [SiliconFlow image model reference](artifact/references/models.md)
- [SiliconFlow image generation API endpoint](https://api.siliconflow.cn/v1/images/generations)
- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-image-gen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands, model parameters, and generated image URL details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SILICONFLOW_API_KEY and may return temporary SiliconFlow image URLs with generation settings.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
