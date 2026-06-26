## Description: <br>
Triggers Botlington's A2A Agent Token Audit for AI agent token efficiency, returning a score, findings, and a prioritized remediation plan with estimated euro savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gary-botlington](https://clawhub.ai/user/gary-botlington) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to submit conversational or direct configuration inputs to Botlington for token-efficiency audits of AI agents. It helps identify model waste, context bloat, tool mismatches, prompt density issues, and repeated work, then returns findings and prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits agent configuration details to an external paid audit provider. <br>
Mitigation: Confirm that Botlington is an acceptable provider before use and remove secrets, customer data, and unnecessary proprietary prompt or configuration details from submitted inputs. <br>
Risk: The workflow requires an API key for Botlington's A2A endpoint. <br>
Mitigation: Keep the API key private, pass it only through the documented x-api-key header or environment handling, and avoid committing it to logs or source files. <br>
Risk: Audit credits are consumed when a consultation starts. <br>
Mitigation: Confirm credit usage and pricing before starting an audit, and resume with the same taskId when continuing an existing conversation. <br>


## Reference(s): <br>
- [Botlington A2A Endpoint](https://botlington.com/a2a) <br>
- [Botlington Agent Card](https://botlington.com/.well-known/agent.json) <br>
- [Sample Botlington Audit](https://botlington.com/audits/stripe) <br>
- [ClawHub Skill Page](https://clawhub.ai/gary-botlington/botlington-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with JSON examples and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes JSON-RPC requests, API-key header usage, SSE streaming, and the expected audit result JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
