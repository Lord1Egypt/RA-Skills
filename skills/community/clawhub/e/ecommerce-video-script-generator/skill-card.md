## Description:

Generates structured 10- or 15-second ecommerce video storyboards from product selling points, category, function, user pain point, and target market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bstory28](https://clawhub.ai/user/bstory28)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, and developers use this skill to turn product metadata and a product image path into localized short-form video storyboard assets for review or downstream video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product metadata and selling_points.json content may be sent to the configured AI provider and later written into local storyboard files.

Mitigation: Use the skill only with product data approved for that provider, review upstream selling_points.json before execution, and inspect storyboard.md before continuing to downstream video generation.

Risk: Upstream usage_instructions are treated as storyboard input, which can carry prompt-injection risk in untrusted pipelines.

Mitigation: Review or sanitize upstream usage_instructions and product metadata before using them to generate final storyboard assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bstory28/skills/ecommerce-video-script-generator)
- [Server-resolved GitHub provenance](https://github.com/BStory28/ecommerce-video-script-generator)
- [Upstream product info generator](https://github.com/BStory28/ecommerce-product-info-generator)
- [Downstream ecommerce video generator](https://github.com/BStory28/ecommerce-video-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON storyboard data and Markdown storyboard tables, with shell command guidance for pipeline execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs storyboard.json for agent or pipeline use and storyboard.md for human review; local file output can use a default or user-specified directory.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
