## Description:

Generates 9:16 vertical high-definition images from text prompts for short drama storyboards, character portraits, and scene illustrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn prompts into vertical images for short-drama keyframes, short-video assets, and novel IP visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and negative prompts are sent to the configured image-generation provider.

Mitigation: Use an HTTPS API_BASE that you control or trust, apply a limited-scope API key with quotas, and avoid confidential prompts unless the provider is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/04-text-to-image)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON object containing an image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured text-to-image provider through API_KEY, API_BASE, and MODEL_NAME.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
