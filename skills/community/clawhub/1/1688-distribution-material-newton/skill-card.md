## Description:

This skill helps agents optimize 1688 distribution materials by editing or generating product images, creating white-background cutouts, optimizing product titles, and generating selling points from 1688 product IDs or image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 sellers, commerce operators, and agents use this skill to produce Chinese product marketing materials, including optimized images, white-background cutouts, titles, and selling-point copy. It supports workflows that start from a 1688 product ID, product link, or image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access keys and ISV tokens may be exposed through chat, command arguments, plaintext files, or command history.

Mitigation: Use the skill only in a trusted local environment, avoid pasting secrets into normal chat, and rotate any AK or ISV token previously entered through chat or command arguments.

Risk: Environment-controlled OPENCLAW_GATEWAY_URL and BASE_URL values may redirect requests to unexpected hosts.

Mitigation: Verify both environment variables before use and clear unexpected overrides before running commands that send authenticated requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-distribution-material-newton)
- [1688 AK configuration portal](https://clawhub.1688.com)
- [AK configuration](references/10_ak_configure.md)
- [Product information query](references/20_product_info.md)
- [Product image query](references/30_product_image.md)
- [Image editing](references/40_image_edit.md)
- [Cutout image generation](references/50_cutout_image.md)
- [Title optimization](references/60_title_optimize.md)
- [Selling-point generation](references/70_selling_point.md)
- [Image optimization workflow](references/80_image_optimize.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Chinese Markdown responses derived from CLI JSON output, with shell commands for AK checks and material optimization actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns success, markdown, and data fields; the agent is instructed to show the markdown field first and keep user prompts unchanged when invoking optimization commands.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
