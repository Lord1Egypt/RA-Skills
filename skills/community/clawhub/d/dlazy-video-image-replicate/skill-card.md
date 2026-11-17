## Description:

Study a user-provided reference image or video, then recreate its look and structure with the user's own subject, product, or characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide a reference image or video and use this skill to create a similar image or video featuring their own subject, product, or characters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms may match requests outside the intended image or video recreation task.

Mitigation: Invoke the skill only when the user clearly asks to recreate or adapt a reference image or video.

Risk: Prompts and attached reference files are sent to dLazy services, and the CLI uses authenticated project actions.

Mitigation: Avoid attaching sensitive media, review the requested action before running it, and use an API key the user is comfortable associating with their dLazy organization.

## Reference(s):

- [dLazy website](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-video-image-replicate)

## Skill Output:

**Output Type(s):** [Images, Videos, Text]

**Output Format:** [Generated image or video media with accompanying text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided reference and subject description; attached files are uploaded to dLazy media storage.]

## Skill Version(s):

1.3.41 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
