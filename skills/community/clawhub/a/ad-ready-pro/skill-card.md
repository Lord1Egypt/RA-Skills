## Description:

Generate professional advertising images from product URLs using the Ad-Ready pipeline on ComfyDeploy, with optional brand profiles, funnel-stage targeting, model or talent references, and multi-format output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Developers, marketers, and creative operators use this skill to prepare and run product advertising image generation from a product URL, brand assets, campaign objective, and optional visual references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary product or image URLs and upload retrieved assets to ComfyDeploy.

Mitigation: Review URLs and assets before execution, avoid auto-fetch for untrusted URLs, and run in an environment with restricted outbound network access where practical.

Risk: Sensitive products, internal URLs, private staging sites, unreleased brand assets, or confidential reference images could be exposed to an external generation service.

Mitigation: Use public or approved assets where possible, and do not run the skill against confidential material without an appropriate review.

Risk: Product scraping may be fragile or blocked, which can produce incorrect product data or lower-quality advertising output.

Mitigation: Provide manually selected product images, logos, and reference assets when possible, and review generated ads before publication.

## Reference(s):

- [Ad-Ready Pro on ClawHub](https://clawhub.ai/pauldelavallaz/skills/ad-ready-pro)
- [Patreon Ad-Ready docs](https://www.patreon.com/posts/from-product-to-149933468)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ComfyDeploy API key and may upload selected product, logo, model, and reference images to ComfyDeploy.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
