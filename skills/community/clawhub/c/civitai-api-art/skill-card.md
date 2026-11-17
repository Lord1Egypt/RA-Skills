## Description:

Generate AI images from text prompts with CivitAI's JavaScript SDK using configurable models, samplers, seeds, steps, LoRA networks, and output settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinnpuru](https://clawhub.ai/user/shinnpuru)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to request CivitAI image generations from prompts and tune common Stable Diffusion parameters such as model, sampler, seed, size, steps, CFG scale, and LoRA networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access and a CivitAI API token to submit image-generation jobs.

Mitigation: Use a dedicated token with limited exposure and keep it in the CIVITAI_API_TOKEN environment variable rather than embedding it in prompts, commands, or files.

Risk: Prompts and generated content are sent to CivitAI and may be governed by CivitAI model permissions, subscriptions, and terms.

Mitigation: Avoid private or sensitive prompt content and confirm that selected models and LoRA networks are permitted for the intended use.

Risk: The script downloads generated images to a user-supplied output path.

Mitigation: Run the skill in a restricted workspace and choose output paths deliberately.

Risk: The npm dependency can change over time if installed without a lockfile.

Mitigation: Pin the civitai package version and use a lockfile for repeatable installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinnpuru/skills/civitai-api-art)
- [Publisher profile](https://clawhub.ai/user/shinnpuru)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command-line examples, console text, generated image URLs, and local image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CivitAI API token in the environment and writes the generated image to the requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
