## Description:

Use this skill to optimize Amazon product listings, generate product images, improve titles, monitor CTR, and automate end-to-end Amazon product optimization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, product managers, and cross-border e-commerce teams use this skill to research product keywords, improve listing titles, generate scene-based product image prompts, and monitor main-image CTR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may update the supplied product JSON/CSV file.

Mitigation: Create a backup or write optimized output to a new file before applying changes to important business data.

Risk: The skill may use external keyword sources and Taobao MCP for image generation.

Mitigation: Review external-service use and generated image outputs before publishing listing changes.

Risk: Optional CTR monitoring may create recurring operational checks.

Mitigation: Confirm the monitoring schedule and disable or adjust daily checks when they are not needed.

## Reference(s):

- [Optimization Guide](references/optimization-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown guidance with structured listing recommendations and JSON/CSV product-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the supplied product JSON/CSV file, use Taobao MCP for image generation, and produce CTR monitoring recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
