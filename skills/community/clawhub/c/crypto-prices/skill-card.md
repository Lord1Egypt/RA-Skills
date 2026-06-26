## Description: <br>
Fetches live cryptocurrency and commodity prices from configured local price providers with caching and fallback behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryandeangraves](https://clawhub.ai/user/ryandeangraves) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users use this skill to retrieve current cryptocurrency and commodity prices for market analysis, reports, or direct price questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad price-related wording may cause an agent to invoke the skill more often than intended. <br>
Mitigation: Use it for explicit cryptocurrency, commodity, market-analysis, report, or direct price-query tasks. <br>
Risk: Price results depend on the referenced local price module and external data providers. <br>
Mitigation: Confirm the local price module comes from the same trusted package and report price unavailable when providers fail. <br>


## Reference(s): <br>
- [Crypto Prices ClawHub listing](https://clawhub.ai/ryandeangraves/crypto-prices) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and formatted price text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces live price lookups, batch price blocks, and unavailable-price messages when providers fail.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
