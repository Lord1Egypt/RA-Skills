## Description: <br>
Human verification for AI agents. Submit claims, draft responses, or observation requests to human domain experts via the 2O API. Returns structured verdicts with confidence scores and evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellshen1992](https://clawhub.ai/user/russellshen1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to submit factual claims, sensitive draft responses, or real-world observation requests for human review through the 2O API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive user text, situational context, addresses, coordinates, or photo requests may be sent to outside human reviewers. <br>
Mitigation: Ask for explicit user approval before each submission, show the exact payload, and redact unnecessary personal, confidential, secret, or regulated data. <br>
Risk: Witness requests can involve observing people or private locations. <br>
Mitigation: Use witness requests only for lawful, consented observations and avoid requests involving people or private spaces without authorization. <br>
Risk: The API examples include paid requests with budgets and urgency settings. <br>
Mitigation: Confirm cost, urgency, tier, and budget before creating a request, and check account balance when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/russellshen1992/2o-verification) <br>
- [2O registration](https://www.2oapi.xyz/register) <br>
- [2O verify endpoint](https://www.2oapi.xyz/api/v1/verify) <br>
- [2O empathy review endpoint](https://www.2oapi.xyz/api/v1/empathize) <br>
- [2O witness endpoint](https://www.2oapi.xyz/api/v1/witness) <br>
- [2O agent balance endpoint](https://www.2oapi.xyz/api/v1/agent/balance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TWO_O_API_KEY and may create paid API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
