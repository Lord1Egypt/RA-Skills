## Description:

Guides agents to create structured commercial and e-commerce image-generation prompts using subject-scene, style-texture, and technical-constraint layers for global and Asian platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and e-commerce operators use this skill to produce platform-specific prompts for product photos, marketing posters, social covers, and commercial AI visuals. It emphasizes aspect ratios, safe areas, negative prompts, and iterative refinements for global and Asian commerce channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts may target the wrong platform, language, aspect ratio, or visual style for a campaign.

Mitigation: Confirm the target marketplace, language, safe-area requirements, and brand direction before using the generated prompt in production creative workflows.

Risk: AI image outputs can contain unusable text artifacts, watermarks, distorted products, or crowded layouts.

Mitigation: Keep the skill's negative prompts, safe zones, and one-variable-at-a-time iteration guidance in the final prompt and review generated images before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fize/skills/commercial-image-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with structured prompt layers and negative constraints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commercial image prompt guidance; it does not execute image generation or request credentials.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
