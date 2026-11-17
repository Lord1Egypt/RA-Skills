## Description:

Search Amazon products and retrieve product details through Amazon Product Advertising API (PA-API) for product discovery, price lookup, and affiliate-link workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akkualle](https://clawhub.ai/user/akkualle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, commerce operators, and affiliate-content agents use this skill to search Amazon.de products, retrieve product details by ASIN, look up prices, and support affiliate-link generation through Amazon PA-API.

### Deployment Geography for Use:

Global, with default configuration for Amazon Germany (Amazon.de).

## Known Risks and Mitigations:

Risk: The skill requires Amazon PA-API credentials and an Amazon Associates partner tag in environment variables.

Mitigation: Confirm the intended Amazon PA-API account and marketplace before use, and provide credentials through managed environment secrets rather than hardcoding them in prompts or files.

## Reference(s):

- [Amazon PA-API Integration on ClawHub](https://clawhub.ai/akkualle/skills/akkualle-amazon-paapi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and product lookup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Amazon PA-API credentials and an Amazon Associates partner tag through environment variables; defaults target Amazon.de unless configured otherwise.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
