## Description:

A workflow for planning marketing brochures, creating full layouts, and producing folded and lifestyle mock-ups after layout approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and designers use this skill to plan corporate, product, event, and service brochures, generate unfolded layouts, and create folded or lifestyle mock-ups after approving the layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports authentication-related CLI actions that are not clearly tied to brochure design, and scanner coverage is incomplete because referenced material was unavailable.

Mitigation: Review the CLI authentication behavior and resolve the missing references before installation; use a rotatable API key and avoid sending sensitive content or media unless appropriate.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-image-marketing-brochure)
- [dLazy website](https://dlazy.com)
- [dLazy CLI project](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Images]

**Output Format:** [Markdown planning and image-generation prompts, plus generated brochure layouts and mock-up images]

**Output Parameters:** [Variable brochure format and panel count]

**Other Properties Related to Output:** [Mock-up generation follows layout approval and uses the approved layout as its visual reference; image generation uses the dLazy service.]

## Skill Version(s):

1.3.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
