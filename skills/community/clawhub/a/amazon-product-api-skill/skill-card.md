## Description:

This skill helps users extract structured product listings from Amazon, including titles, ASINs, prices, ratings, and specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and ecommerce operators use this skill to run BrowserAct-backed Amazon product searches and collect structured listing data for market research, competitor monitoring, product catalog enrichment, price tracking, and localized research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill unsafely tells users they may provide a BrowserAct API key in chat.

Mitigation: Configure BROWSERACT_API_KEY only through the local environment or an approved secret manager, avoid pasting the key into chat, and rotate any key that has already been shared.

Risk: Running the skill sends product search inputs and the BrowserAct bearer token to BrowserAct's API.

Mitigation: Review intended search terms before execution and use an approved BrowserAct account and credential-handling process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-product-api-skill)
- [BrowserAct API key setup](https://www.browseract.com/reception/integrations)
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured product data printed as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; sends product search inputs and a BrowserAct bearer token to BrowserAct's API.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
