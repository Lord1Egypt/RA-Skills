## Description:

Generates Happy Horse 1.0 videos from text prompts, first frames, reference images, or existing videos, with modes for text-to-video, image-to-video, reference-to-video, and video editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to request short generated videos or edits through dLazy's hosted Happy Horse service, using text, images, or video as inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied local media are sent to dLazy's hosted service, and local media may be uploaded for processing.

Mitigation: Use only prompts and media you are comfortable sharing with the service; avoid uploading sensitive content unless authorized.

Risk: The scan had partial coverage and its reported examples did not demonstrate the advertised video features.

Mitigation: Check the CLI help and verify the needed generation mode with non-sensitive input before relying on it for a production workflow.

Risk: The CLI requires a dLazy API key.

Mitigation: Use the key only with the intended account, store it through the documented login flow or environment variable, and rotate or revoke it if exposed.

## Reference(s):

- [dLazy CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)
- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-happyhorse-1-0)

## Skill Output:

**Output Type(s):** [Video, JSON]

**Output Format:** [Generated media returned as hosted URLs in a JSON response; media can optionally be saved to a local file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-video, first-frame-to-video, reference-to-video, and video editing; resolution, duration, and aspect ratio options vary by mode.]

## Skill Version(s):

1.3.45 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
