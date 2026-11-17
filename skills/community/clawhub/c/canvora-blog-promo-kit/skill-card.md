## Description:

Turn one published article URL into a visual kit with Canvora, including blog imagery, an Open Graph share card, and social promotion assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canvora](https://clawhub.ai/user/canvora)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to turn a published article into on-page images, an Open Graph card, and channel-specific social promotion assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generating assets fetches article content from its public URL for external processing through Canvora.

Mitigation: Use an article URL suitable for external processing and specify whether the request is for assets only or also publication through a connected posting tool.

Risk: A multi-asset kit can consume credits and may be incomplete if the available balance runs out during generation.

Mitigation: Set a credit budget, total the planned generation cost, and check the Canvora balance before starting.

## Reference(s):

- [Canvora agent documentation](https://canvora.ai/for-agents)
- [ClawHub release](https://clawhub.ai/canvora/skills/canvora-blog-promo-kit)

## Skill Output:

**Output Type(s):** [Image assets, Text guidance, Shell commands]

**Output Format:** [Generated image assets with CLI instructions and output links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formats include blog headers, featured images, Open Graph cards, banners, and social assets; sizes and slide counts depend on the requested formats.]

## Skill Version(s):

1.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
