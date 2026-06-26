## Description: <br>
This skill helps agents extract structured Amazon product listings, including titles, ASINs, prices, ratings, and product attributes, through BrowserAct. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and market-research agents use this skill to search Amazon listings and collect structured product data for pricing, competitor monitoring, catalog enrichment, rating analysis, and localized product research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon search terms and related parameters are sent to BrowserAct. <br>
Mitigation: Use a dedicated, revocable BrowserAct API key through the environment or a secure secret manager, and avoid placing the key in chat, logs, or source code. <br>
Risk: The skill runs an external BrowserAct workflow that may take several minutes and can fail because of network, authorization, or task-status errors. <br>
Mitigation: Monitor status output, do not retry invalid authorization failures, and limit automatic retries for other failures to one attempt. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/phheng/amazon-product-api-skill) <br>
- [BrowserAct Console integrations](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with status logs and structured product-data output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python and BROWSERACT_API_KEY; accepts keywords, brand, page count, and language.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
