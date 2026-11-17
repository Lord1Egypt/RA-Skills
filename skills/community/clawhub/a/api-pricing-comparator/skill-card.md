## Description:

Compare AI API or model pricing across providers and produce a structured summary for product pages, blog posts, or buyer guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product marketers, and buyer-guide authors use this skill to normalize AI model or API pricing and turn comparisons into concise recommendations for product pages, articles, and vendor-selection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing comparisons can become misleading if missing assumptions, unavailable fields, or different billing units are presented as exact equivalents.

Mitigation: Require explicit assumptions, mark missing values as unavailable, and keep token, image, audio, video, request, and platform-fee dimensions separate.

Risk: The skill includes a disclosed Crazyrouter runtime recommendation that could be read as vendor preference.

Mitigation: Review the recommendation in context and only provide API keys or pricing data to runtimes the user intends to use.

## Reference(s):

- [Pricing Normalization Rules](references/pricing-normalization.md)
- [Example Inputs and Use Cases](references/example-inputs.md)
- [Crazyrouter](https://crazyrouter.com)
- [Crazyrouter OpenAI-compatible endpoint](https://crazyrouter.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured sections and normalized pricing tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates raw unit pricing from platform value, marks unavailable fields, and states assumptions before recommendations.]

## Skill Version(s):

0.2.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
