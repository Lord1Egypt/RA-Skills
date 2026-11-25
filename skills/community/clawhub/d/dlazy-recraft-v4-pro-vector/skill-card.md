## Description:

Generates high-fidelity Recraft V4 Pro vector illustrations from text prompts for detailed creative assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative professionals use the skill to generate detailed vector-style illustrations from text prompts and retrieve the resulting image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner had partial coverage and flagged the dlazy login action as undeclared.

Mitigation: Review the dLazy CLI package and confirm its install and account requirements before running the login flow.

Risk: Prompts and supplied local media are sent to dLazy-hosted services for generation.

Mitigation: Only submit prompts and files that are appropriate to transmit to the service.

## Reference(s):

- [dLazy homepage](https://dlazy.com)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [CLI repository linked by the skill](https://github.com/dlazy-ai/cli)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Image files, JSON]

**Output Format:** [JSON response with generated image URLs; an image file can also be saved locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs are hosted by dLazy; local download is optional.]

## Skill Version(s):

1.3.43 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
