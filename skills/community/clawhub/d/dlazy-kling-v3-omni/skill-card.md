## Description:

Generates videos with Kling v3 Omni from prompts and multimodal references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use the skill to generate videos from text prompts and image or video references through Kling v3 Omni.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review noted a mismatch between the skill’s video-generation purpose and a supplied login command; the concern was not confirmed as malicious, and the benign assessment has medium confidence.

Mitigation: Review the CLI package and referenced paths before installing, as the security analysis is incomplete.

Risk: Prompts and local image, video, or audio files supplied to the skill are sent to dLazy hosted services for processing.

Mitigation: Avoid sending sensitive prompts or media unless the user is comfortable with that service processing and storing the content.

## Reference(s):

- [dLazy CLI project page](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service website](https://dlazy.com)
- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-kling-v3-omni)

## Skill Output:

**Output Type(s):** [Video, JSON, Guidance]

**Output Format:** [Generated video assets with JSON result metadata; task identifiers for asynchronous generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports prompt and image/video references; generated assets are returned as hosted URLs and can optionally be saved locally.]

## Skill Version(s):

1.3.40 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
