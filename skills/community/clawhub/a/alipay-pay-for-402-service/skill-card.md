## Description: <br>
Guides an agent through an Alipay CLI-based A402 payment workflow when an HTTP request returns 402 Payment Required, including payment initiation, status checking, resource retry, and fulfillment acknowledgement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an HTTP 402 response requires an A402 buyer payment flow. It helps the agent collect the Payment-Needed header, run the Alipay payment CLI, wait for user payment confirmation, retry the protected resource request, and acknowledge fulfillment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can initiate real payment activity through an external Alipay CLI. <br>
Mitigation: Review the merchant, amount, and authorization prompts before paying, and continue only after explicit user payment confirmation. <br>
Risk: Payment links, payment proofs, feedback text, and purchased resource data may be sensitive. <br>
Mitigation: Avoid persistent logging or forwarding outside the intended channels, and do not submit feedback text containing secrets or unrelated personal information. <br>
Risk: Shell commands and file paths are part of the workflow. <br>
Mitigation: Use the fixed package version and integrity check, validate file names, trade numbers, and resource URLs, and reject unsafe parameters before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yun520-1/alipay-pay-for-402-service) <br>
- [Payment Skills Homepage](https://github.com/alipay/payment-skills) <br>
- [Alipay Agent Payment npm Package](https://www.npmjs.com/package/@alipay/agent-payment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and CLI output, with possible JSON responses and MEDIA lines from the payment CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include payment status, payment links, QR-code media paths, trade numbers, and purchased resource content returned by the CLI workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
