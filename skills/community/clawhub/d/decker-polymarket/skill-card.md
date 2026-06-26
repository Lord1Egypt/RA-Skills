## Description: <br>
Helps agents handle Polymarket prediction-market requests through Decker, including market search, category and event lookup, market slug details, and YES/NO order requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigshow](https://clawhub.ai/user/gigshow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or developers using Decker can ask an agent to find Polymarket markets, inspect categories, events, and market slugs, and prepare YES/NO order requests. The skill is intended for Decker-connected workflows that require manual confirmation of trading details before orders are submitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real Polymarket trades, so incorrect market slugs, sides, quantities, or prices can cause financial loss. <br>
Mitigation: Verify every market slug, YES/NO outcome, quantity, price, and wallet manually before submitting an order. <br>
Risk: The setup flow asks users to store a Polygon wallet private key with Decker, creating wallet-level authority risk. <br>
Mitigation: Use a dedicated low-balance wallet for Polymarket, and do not provide a primary wallet private key or seed phrase. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gigshow/decker-polymarket) <br>
- [Decker API endpoint](https://api.decker-ai.com) <br>
- [Polymarket](https://polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Markdown text with API request examples and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Decker order-request URLs, market slug guidance, YES/NO outcome selection, quantity, and optional limit price.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
