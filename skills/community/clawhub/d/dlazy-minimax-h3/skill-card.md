## Description:

MiniMax Hailuo omni-modal video model with native stereo audio, producing 5–15 second clips at up to 2K, with text-to-video, first/last frame transitions, and multi-asset references for character and scene consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to generate short MiniMax Hailuo videos from text prompts, first and last frames, or image, video, and audio references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt and input media are sent to dLazy's hosted service, and local media paths may be uploaded for processing.

Mitigation: Review the service details and avoid sending prompts or media that you do not want processed by the hosted service.

Risk: The skill advertises 4K as an option, while the release description summarizes output up to 2K and scanner confidence is medium.

Mitigation: Confirm supported resolution and service behavior before relying on 4K output.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-minimax-h3)
- [dLazy CLI project page](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video, JSON, Shell commands]

**Output Format:** [Generated video assets and JSON result metadata, including hosted asset URLs or asynchronous task IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable generation mode, duration, aspect ratio, and resolution; input media files may be uploaded to the hosted service.]

## Skill Version(s):

1.2.38 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
