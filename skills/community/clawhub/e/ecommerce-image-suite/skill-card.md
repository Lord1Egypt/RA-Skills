## Description:

Helps agents create ecommerce image suites from product images and selling points for domestic Chinese and cross-border marketplace listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzj177](https://clawhub.ai/user/wzj177)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce operators use this skill to analyze product imagery, generate product-selling-point prompts, call a selected image generation provider, and overlay listing copy for platform-specific image sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product descriptions and prompts may be sent to the selected image provider or configured proxy.

Mitigation: Use the skill only with providers and proxy endpoints you trust, and avoid submitting sensitive product data unless provider handling is acceptable.

Risk: API keys and provider-check output may expose credential details if copied into logs or shared channels.

Mitigation: Use low-privilege provider keys and avoid logging or sharing provider-check output.

Risk: Custom base URLs and provider-returned image URLs expand network trust boundaries.

Mitigation: Avoid custom base URLs unless controlled and trusted, and restrict runs to dedicated output directories until endpoint validation and URL-fetch safeguards are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzj177/skills/ecommerce-image-suite)
- [Platform specifications](artifact/references/platforms.md)
- [Image type specifications](artifact/references/image-types.md)
- [Provider configuration reference](artifact/references/providers.md)
- [Analysis prompt reference](artifact/references/analysis-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON inputs, shell commands, generated image files, and summary JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider credentials; writes raw and final image outputs plus generation and overlay summaries to configured output directories.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
