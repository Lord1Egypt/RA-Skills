## Description:

Generate advertising images automatically from a product URL and brand profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

External marketers, creative teams, and developers use Ad-Ready to generate product advertising images from ecommerce URLs, brand profiles, and funnel-stage objectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product URLs, product images, logos, model or reference images, and generated outputs may be sent to ComfyDeploy and related logo services.

Mitigation: Use the skill only with assets approved for external processing, and avoid private, internal, or credentialed URLs, especially with auto-fetch enabled.

Risk: The workflow strongly preserves human likeness and sensitive traits in generated ads.

Mitigation: Use only model or reference images with appropriate rights and consent for commercial advertising.

Risk: Auto-fetch can retrieve arbitrary product pages and logo assets.

Mitigation: Prefer explicit product images when possible, review URLs before execution, and avoid sources that may expose confidential or restricted content.

## Reference(s):

- [Ad-Ready ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/ad-ready)
- [ComfyDeploy queue endpoint used by the skill](https://api.comfydeploy.com/api/run/deployment/queue)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance and shell commands, with PNG image files produced by the generation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a product URL, product image, brand profile, prompt profile, output path, and ComfyDeploy API key; logo, model, reference image, aspect ratio, language, and creative brief are optional.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
