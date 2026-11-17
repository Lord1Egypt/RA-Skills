## Description:

A professional product image generation skill purpose-built for the Amazon e-commerce platform, producing listing and A+ content images aligned with Amazon image guidelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and product-content teams use this skill to plan and generate main and secondary listing images, product infographics, lifestyle and detail shots, and A+ Brand Content modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports that the CLI login command’s connection to the advertised image-generation purpose is unclear and that scanner coverage was partial; its benign verdict is not a guarantee of safety.

Mitigation: Review the CLI authentication flow and credential handling before use, and use the documented key rotation or revocation controls if needed.

Risk: The skill sends prompts and supplied media to dLazy-hosted services for processing.

Mitigation: Avoid sending confidential product or customer material unless it is approved for processing by the hosted service.

## Reference(s):

- [dLazy CLI repository (CLI reference; skill provenance unavailable)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Image-generation requests]

**Output Format:** [Markdown plans and prompts, CLI commands, and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation is guided step by step; a full suite typically contains one main image, six secondary images, and eight A+ modules.]

## Skill Version(s):

1.3.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
