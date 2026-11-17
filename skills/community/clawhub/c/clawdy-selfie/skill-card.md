## Description:

Generate a Clawdy selfie with the installed local helper script and the configured FAL_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill when Clawdy is asked for a selfie, photo, mirror picture, outfit shot, location selfie, or related media. The skill generates reference-based images and includes a video workflow that can send generated media to OpenClaw channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports under-disclosed video generation, third-party uploads, channel posting, and unsafe command execution paths.

Mitigation: Review the skill before installing, restrict use to trusted prompts and channels, and fix command handling before broad deployment.

Risk: The video workflow can upload the reference image to third-party hosts and uses a separate Seedance API key.

Mitigation: Use tightly scoped credentials, prefer a controlled CLAWDY_REFERENCE_URL, and avoid sensitive reference images.

Risk: Generated media is sent to OpenClaw channels and temporary files are created locally.

Mitigation: Confirm destination channels before execution and add cleanup controls for temporary media files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/clawdy-selfie)
- [Publisher profile](https://clawhub.ai/user/x-rayluan)
- [fal.ai key dashboard](https://fal.ai/dashboard/keys)
- [Grok Imagine image endpoint](https://fal.run/xai/grok-imagine-image)
- [Grok Imagine image edit endpoint](https://fal.run/xai/grok-imagine-image/edit)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command execution and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images or videos may be posted to OpenClaw channels and saved as temporary local media files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
