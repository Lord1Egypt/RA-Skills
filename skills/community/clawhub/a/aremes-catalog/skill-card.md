## Description: <br>
Query Ryan Seslow's art & design catalog, look up individual works, check x402 quotes, and log purchase intent via the AREMES autonomous commerce agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanseslow](https://clawhub.ai/user/ryanseslow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse Ryan Seslow's art and design catalog, inspect individual works, request x402 quotes, and prepare Stripe or USDC purchase workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit buyer contact details, create purchase intents, verify orders, and initiate Stripe or USDC payment workflows. <br>
Mitigation: Require explicit user approval before sending buyer information, creating a purchase intent, verifying an order, or starting any payment step. <br>
Risk: Quotes, payment amounts, recipient details, and order windows can affect real purchases. <br>
Mitigation: Confirm product ID, license tier, quoted amount, recipient wallet or checkout URL, and expiration time with the user before proceeding. <br>
Risk: Catalog browsing and quote lookup are lower risk, but later workflow steps can disclose contact details or commit a buyer to checkout. <br>
Mitigation: Limit unaudited use to browsing and quote retrieval, and pause for approval before any workflow that records intent or payment evidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryanseslow/aremes-catalog) <br>
- [Ryan Seslow Catalog](https://ryanseslow.com/catalog.json) <br>
- [AREMES Agent Endpoint](https://aremes-enterprises.com/agent.json) <br>
- [AREMES On-chain Identity](https://agentfolio.bot/@aremes) <br>
- [Catalog REST API](https://ryanseslow.com/wp-json/rsmad/v1/catalog) <br>
- [x402 Quote API](https://ryanseslow.com/wp-json/rsmad/v1/x402/quote) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with HTTP examples and JSON request and response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include catalog records, signed quotes, checkout URLs, order identifiers, and payment status data from public commerce endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
