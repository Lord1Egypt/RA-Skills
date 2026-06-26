## Description: <br>
Queries Baidu Youjia for car brands, series, model details, dealer pricing, recent transaction prices, discounts, insurance costs, rankings, and related vehicle information by query and optional city. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changxueyi](https://clawhub.ai/user/changxueyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer vehicle-shopping questions such as model pricing, local dealer quotes, discounts, estimated taxes and insurance, and recent owner transaction references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Baidu/Qianfan API key and sends requests to Baidu's car-price lookup endpoint. <br>
Mitigation: Store BAIDU_API_KEY only in the agent or OpenClaw configuration, keep it out of source control and logs, and rotate the key if exposure is suspected. <br>
Risk: Vehicle query and city values are sent to an external service and may reveal user interests or location context. <br>
Mitigation: Avoid entering sensitive personal details in query or city fields and use only the minimum information needed for the lookup. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/changxueyi/baidu-youjia-car) <br>
- [API key setup guide](references/apikey-fetch.md) <br>
- [Baidu Qianfan API key console](https://console.bce.baidu.com/qianfan/ais/console/apiKey) <br>
- [Baidu Qianfan askprice endpoint](https://qianfan.baidubce.com/v2/tools/clue/askprice) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown-formatted text from a Python command that accepts JSON input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a BAIDU_API_KEY environment variable; input JSON must include query and may include city.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact _meta.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
