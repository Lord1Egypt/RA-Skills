## Description:

A structured workflow skill dedicated to social-media carousel design. The core method is 'decide intent first, then execute,' using a 'single-confirmation + cover-first' two-phase flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social content creators use this skill to plan carousel narratives, define each slide's role and copy, and guide cover-first generation of a consistent slide set with confirmation between phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires dLazy authentication, and prompts or supplied media may be sent to dLazy-hosted services; the security assessment also flags that the authentication setup is not clearly declared for the carousel-design purpose.

Mitigation: Review the dLazy CLI authentication and data-handling details before use, and submit only prompts and assets approved for that service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-image-social-carousel)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Images]

**Output Format:** [Markdown planning tables and structured slide guidance; carousel image assets via the dLazy CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cover-first workflow with user confirmation before generation; image generation requires dLazy CLI authentication.]

## Skill Version(s):

1.3.45 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
