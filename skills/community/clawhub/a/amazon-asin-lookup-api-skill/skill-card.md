## Description: <br>
Looks up Amazon products by ASIN through BrowserAct and returns structured product details such as title, price, ratings, brand, availability, and descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, catalog operators, and market analysts use this skill to enrich product records, compare prices, monitor ratings, and validate Amazon ASINs with structured product metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a BrowserAct API key, and the security summary flags unsafe guidance around handling that key. <br>
Mitigation: Configure the key through environment variables or secret storage, and do not paste it into chat, prompts, logs, or shared transcripts. <br>
Risk: Lookup requests are sent to BrowserAct to retrieve Amazon product information. <br>
Mitigation: Use the skill only when sending ASIN lookup requests to BrowserAct is acceptable for the user's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/amazon-asin-lookup-api-skill) <br>
- [BrowserAct integration console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Terminal logs followed by structured product data as text or JSON] <br>
**Output Parameters:** [1D; ASIN input string] <br>
**Other Properties Related to Output:** [Requires Python, BROWSERACT_API_KEY, network access to BrowserAct, and polling until the lookup task finishes.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
