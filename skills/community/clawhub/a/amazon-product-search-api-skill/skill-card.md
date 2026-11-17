## Description:

This skill helps agents extract structured product listing data from Amazon search results through BrowserAct's Amazon Product Search API template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market research teams use this skill to search Amazon by keyword, brand, count, and language, then collect product titles, URLs, prices, ratings, review counts, sales estimates, availability, and shipping details for catalog, pricing, or competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BrowserAct API key and the security evidence warns against sharing that key in chat.

Mitigation: Configure BROWSERACT_API_KEY through the environment or an approved secret manager, and rotate any key that was previously shared in a conversation.

Risk: Amazon search terms, brand filters, and market-research parameters are sent to BrowserAct.

Mitigation: Install and run the skill only when users are comfortable sending those inputs to BrowserAct; avoid sensitive internal research terms unless approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-product-search-api-skill)
- [BrowserAct integration console](https://www.browseract.com/reception/integrations)
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text stream with status logs and structured product-result data, typically JSON-like or API-returned string output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY; polls BrowserAct until task completion and prints results.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
