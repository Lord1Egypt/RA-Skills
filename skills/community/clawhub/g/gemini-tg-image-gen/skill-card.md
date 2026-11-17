## Description:

Generate images via OpenRouter (google/gemini-2.5-flash-image) and send them to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drones277](https://clawhub.ai/user/drones277)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to generate AI images from a prompt through OpenRouter and deliver the resulting image file to Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image-fetching script can follow arbitrary URLs returned by the model, which creates network and data-exposure risk.

Mitigation: Accept only trusted structured image outputs or validated inline image data, enforce content type and size limits, and avoid sensitive prompts or internal-network environments until URL fetching is constrained.

Risk: Generated images are written to local temporary storage for Telegram delivery.

Mitigation: Delete temporary image files after sending and avoid prompts or outputs that contain sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drones277/skills/gemini-tg-image-gen)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON path output from the generation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and produces local image file paths for Telegram delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
