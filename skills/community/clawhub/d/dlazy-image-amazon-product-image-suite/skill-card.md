## Description:

Generates Amazon product listing images and A+ Brand Content layouts guided by the platform's stated image requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, brand teams, and creative operators use this skill to plan product listing image sets and A+ content for product detail pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a benign verdict with medium confidence and a partial scan; it flags an unexplained `dlazy login` step and incomplete resolution of package and runtime references.

Mitigation: Review the CLI package and its authentication behavior before installation, and use a rotatable API key stored with appropriate account permissions.

Risk: The skill says prompts and local media files are sent to dLazy-hosted services for generation.

Mitigation: Avoid submitting confidential product information or media unless your organization permits sharing it with that service.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dlazyai/skills/dlazy-image-amazon-product-image-suite)
- [CLI repository listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Generated image files plus Markdown status and checklists, with CLI instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Amazon image specifications and staged image-set delivery; image generation requires the configured dLazy service.]

## Skill Version(s):

1.3.45 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
