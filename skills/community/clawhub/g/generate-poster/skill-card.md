## Description:

Generate Poster helps agents generate ecommerce product main images and detail-page posters through the Flyelep API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnwanj](https://clawhub.ai/user/cnwanj)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agents use this skill to turn product descriptions and optional reference image URLs into product main images or detail-page poster image URLs for marketplaces such as Amazon, Taobao, and TikTok Shop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation prompts, reference image URLs, and the Flyelep API key are sent to Flyelep.

Mitigation: Use a dedicated API key and avoid sensitive product, customer, or unreleased business data in prompts or image URLs unless that transfer is approved.

Risk: The Flyelep API requires the secretKey in the JSON request body, which can expose credentials if request bodies are logged.

Mitigation: Provide the key dynamically at runtime, do not hardcode real keys in examples or skill code, and avoid logging full request bodies.

Risk: Image generation can take several minutes or return temporary service errors.

Mitigation: Use the documented 300-600 second timeout, handle empty or error responses, and retry later when the service reports high concurrency.

## Reference(s):

- [Generate Poster on ClawHub](https://clawhub.ai/cnwanj/skills/generate-poster)
- [Flyelep Platform](https://www.flyelep.cn)
- [Flyelep Poster Generation API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/generate)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and returned image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns semicolon-delimited image URLs from Flyelep; generation requests can take 300-600 seconds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
