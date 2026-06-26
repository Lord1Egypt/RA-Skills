## Description: <br>
Extracts structured Amazon product reviews by ASIN through BrowserAct's Amazon Reviews API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to collect Amazon product review text, ratings, verified-purchase status, reviewer profile links, country data, and related attributes for market research, competitor analysis, sentiment monitoring, and product feedback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests and ASINs are processed by BrowserAct, and returned review data may include reviewer profile links and country data. <br>
Mitigation: Use the collected review data only for the intended review-extraction task and handle it in line with privacy, platform, and compliance expectations. <br>
Risk: A missing or invalid BROWSERACT_API_KEY prevents successful execution. <br>
Mitigation: Check that BROWSERACT_API_KEY is configured before running, and do not retry when the response reports invalid authorization. <br>
Risk: The external BrowserAct workflow may take several minutes or fail because of service or network conditions. <br>
Mitigation: Monitor timestamped status logs and retry non-authorization failures once before reporting the error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/amazon-reviews-api-skill) <br>
- [BrowserAct Console integrations](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Terminal status logs followed by structured review data as text or JSON from BrowserAct.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python, BROWSERACT_API_KEY, and an Amazon ASIN; the script polls BrowserAct until the workflow finishes.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
