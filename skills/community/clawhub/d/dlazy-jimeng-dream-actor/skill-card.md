## Description:

Convert static character images into vivid action videos with Jimeng Dream Actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn a static character image into an action video by providing a prompt and image to Jimeng Dream Actor through dLazy. Developers can invoke the skill through the dLazy CLI and receive a generated media result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and local image or video files are sent to dLazy's hosted API and media storage for generation.

Mitigation: Use only prompts and media you are authorized to share, and avoid uploading sensitive content unless the service is approved for it.

Risk: The CLI uses a dLazy API key saved in the local CLI configuration.

Mitigation: Keep the key private and rotate or revoke it from the dLazy account dashboard if it is exposed.

## Reference(s):

- [dLazy service homepage](https://dlazy.com)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-jimeng-dream-actor)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Video files]

**Output Format:** [JSON result envelope with generated media URLs; optionally a saved media file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an asynchronous task identifier; generated media is hosted remotely or saved to a requested path.]

## Skill Version(s):

1.3.41 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
