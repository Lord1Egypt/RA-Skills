## Description:

GetPost is an API platform for bots and AI agents that provides email, SMS, search, scraping, AI/LLM inference, image and video generation, domains, and shipping labels through one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dommholland](https://clawhub.ai/user/dommholland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to understand and draft requests for GetPost APIs that let agents send messages, search or scrape the web, call AI models, manage domains and DNS, buy shipping labels, and monitor balances, logs, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers paid operations such as buying credits, registering domains, and purchasing shipping labels.

Mitigation: Require explicit user confirmation before purchases, top-ups, domain registration, DNS changes, or label creation.

Risk: The skill covers externally visible actions such as sending email or SMS and registering webhooks.

Mitigation: Confirm recipients, webhook URLs, message contents, and expected effects before submitting requests.

Risk: The skill requires a GetPost bearer token for authenticated API operations.

Mitigation: Store the token in a secret manager or environment variable and avoid exposing it in prompts, generated files, or logs.

Risk: The security summary says the skill exposes destructive account, webhook, domain, and DNS actions without enough user-control guidance.

Mitigation: Require explicit confirmation before deleting accounts or webhooks and before creating, updating, or deleting DNS records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dommholland/skills/getpost)
- [GetPost OpenAPI Specification](https://getpost.dev/api/openapi.json)
- [GetPost Pricing](https://getpost.dev/api/pricing)
- [GetPost API Base URL](https://getpost.dev/api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with endpoint summaries and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples for paid or externally visible GetPost operations; users should supply and protect their own API credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
