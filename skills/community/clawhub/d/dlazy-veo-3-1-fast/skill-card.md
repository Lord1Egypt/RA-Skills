## Description:

Fast response and generation of short videos with Google Veo 3.1 Fast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can create short videos from text prompts or supplied frames, or extend an existing video, through dLazy's hosted generation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and local image, video, or audio inputs are sent to dLazy's hosted API or media storage.

Mitigation: Avoid sending confidential material and review dLazy's service terms and data handling before use.

Risk: The security review is partial and does not establish how the login step supports video generation.

Mitigation: Review the CLI login flow and disclosures, and use the service only if you trust the dLazy CLI and API.

## Reference(s):

- [dLazy CLI source code (metadata link)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Video, JSON, Files]

**Output Format:** [JSON response with generated media URLs, or a saved media file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation mode, duration, aspect ratio, and resolution are configurable; asynchronous jobs can return a task identifier.]

## Skill Version(s):

1.3.40 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
