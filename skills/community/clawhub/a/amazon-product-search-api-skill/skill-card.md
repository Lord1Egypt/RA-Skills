## Description: <br>
This skill helps agents search Amazon product listings through BrowserAct using keywords, brand filters, result limits, and language settings, then return product details such as titles, URLs, ratings, prices, availability, delivery information, and best-seller status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to collect Amazon product search data for market research, competitive monitoring, catalog discovery, pricing intelligence, and localized product availability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a BrowserAct API key. <br>
Mitigation: Keep BROWSERACT_API_KEY in the environment and do not paste the key into chat or command arguments. <br>
Risk: Search keywords, brand filters, limits, and language settings are sent to BrowserAct for Amazon product searches. <br>
Mitigation: Use only product research terms that are approved to share with BrowserAct. <br>
Risk: The script polls BrowserAct until completion and may run longer than expected. <br>
Mitigation: Monitor status logs and stop the process manually if polling continues beyond the expected task duration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/phheng/amazon-product-search-api-skill) <br>
- [BrowserAct Console](https://www.browseract.com/reception/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with status logs and product result data; successful responses may include structured JSON-like product fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python and BROWSERACT_API_KEY. The script sends keywords, brand, limit, and language to BrowserAct, polls for completion, and prints the returned product data.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
