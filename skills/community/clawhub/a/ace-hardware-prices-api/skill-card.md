## Description:

Retrieves current Ace Hardware US store prices, inventory, weekly ads, product and store details, deals, and paint colors through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping assistants use the skill to look up Ace Hardware prices for a selected store, check local inventory and weekly ads, and retrieve product, store, deal, and paint-color details.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: API requests send their query and store details to Scavio and use an API key.

Mitigation: Review request details, avoid sending sensitive personal information, and keep SCAVIO_API_KEY in an environment variable or secret store rather than source control.

## Reference(s):

- [Scavio Ace Hardware API overview](https://scavio.dev/acehardware-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api)
- [Product details and store pricing](https://scavio.dev/docs/acehardware-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api)
- [Store inventory](https://scavio.dev/docs/acehardware-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api)
- [Weekly ads](https://scavio.dev/docs/acehardware-weekly-ad?utm_source=agent-skills&utm_medium=skill&utm_campaign=ace-hardware-prices-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [JSON data with Markdown guidance and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [US only; prices, inventory, and weekly ads are store-specific and time-sensitive.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
