## Description:

AIGC image generation assistant that creates images from text prompts and supports negative prompts, aspect ratios, and batch generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gushenjie](https://clawhub.ai/user/gushenjie)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use this skill to submit text-to-image requests, poll for generated image results, and deliver generated images through configured channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images may be transferred to Feishu and an external OSS service.

Mitigation: Disclose and control transfer destinations, and require explicit user approval before sending private prompts or generated images externally.

Risk: The release includes a plaintext bearer token that should be considered compromised.

Mitigation: Remove the token from the artifact, rotate it, and load credentials only from a secure environment or secret store.

Risk: Server-supplied image URLs are fetched without validation.

Mitigation: Validate allowed URL schemes and hosts before downloading or forwarding generated images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gushenjie/skills/aigc-bak)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Console text with image URLs, delivery status, and optional local image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload generated images to OSS and send them through Feishu when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
