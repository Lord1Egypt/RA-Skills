## Description: <br>
This skill helps agents query Juhe's paid 5G cell-tower location service with MCC, MNC, LAC/TAC, and CI values, then hands the HTTP 402 payment flow to Alipay before returning location data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to resolve provided cell-tower identifiers into static location details for base-station verification, device-location parsing, and nearby-service workflows. Use it only when the user supplies or confirms the required MCC, MNC, LAC/TAC, and CI values and intends to pay for the lookup. <br>

### Deployment Geography for Use: <br>
Global; service examples and carrier-code guidance in the artifact are China-focused. <br>

## Known Risks and Mitigations: <br>
Risk: Queries send user-provided cell-tower parameters to Juhe and may incur payment through Alipay. <br>
Mitigation: Before each query, confirm the MCC, MNC, LAC/TAC, and CI values, disclose the provider submission, and review the Alipay order details before approving payment. <br>
Risk: Cell-tower location lookups can be misused for unauthorized location inference. <br>
Mitigation: Use the skill only for user-authorized lookups and decline requests that seek illegal tracking or lack the required base-station parameters. <br>
Risk: Changing the request parameters or HTTP 402 payment response can break the paid lookup workflow. <br>
Mitigation: Preserve the submitted JSON parameters and pass the full 402 Payment-Needed response to the Alipay payment skill without alteration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/cell-location) <br>
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples plus curl command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided cell-tower identifiers and an Alipay payment handoff for HTTP 402 responses.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
