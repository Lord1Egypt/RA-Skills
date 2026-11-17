## Description:

Generates videos with Kling v3 from text prompts or reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate Kling v3 videos from text prompts or reference images through dLazy's hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete, with referenced CLI installation and service details unavailable; the login behavior also warrants review in the context of a video-generation skill.

Mitigation: Before installing or authenticating, review the pinned dLazy CLI package and service details, and confirm the login flow is expected. Avoid sending prompts or media until you are comfortable with the service receiving them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-kling-v3)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)
- [dLazy service homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Video files, JSON]

**Output Format:** [Generated video assets with JSON task and result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-video and image-to-video; generated assets are returned as hosted URLs.]

## Skill Version(s):

1.3.41 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
