## Description:

Text-to-vector model that outputs SVG results for logos, icons, and scalable design assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use the skill to create scalable logos, icons, and other design assets from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and medium confidence, and flags login or authentication commands in a skill described as generating SVGs.

Mitigation: Review the CLI and credential workflow before installing or configuring it; use the documented user-scoped credential storage and revoke any exposed key.

Risk: Prompts and supplied media are sent to dLazy hosted services, and local media paths are uploaded for processing.

Mitigation: Avoid sending sensitive or restricted prompts and files unless their use with the service is approved.

## Reference(s):

- [Skill release page](https://clawhub.ai/dlazyai/skills/dlazy-recraft-v4-vector)
- [dLazy CLI project homepage](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JSON response with a generated image URL; optionally a locally saved image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aspect ratio is configurable; asynchronous generation can return a task ID.]

## Skill Version(s):

1.3.39 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
