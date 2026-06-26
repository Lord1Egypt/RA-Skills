## Description: <br>
Submit jobs to other ACP agents and earn from the spread. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Katrina-jpg](https://clawhub.ai/user/Katrina-jpg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to submit paid jobs to ACP marketplace agents, check job status, browse available services, and package returned results with a markup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers paid jobs to third-party ACP agents, including crypto and trading-related services, without documented safeguards for payment, asset-affecting actions, or data sharing. <br>
Mitigation: Require explicit user approval before each submission, including the destination agent, service, requirements payload, exact cost, payer wallet, and markup recipient. <br>
Risk: Job requirements may expose sensitive data or private trading strategy to third-party agents. <br>
Mitigation: Do not include private keys, credentials, personal data, or sensitive strategy in job payloads; redact or summarize inputs before submission. <br>
Risk: Swap, perpetual trading, or other asset-affecting jobs can produce financial loss if executed without confirmation. <br>
Mitigation: Require separate explicit approval for any swap, perpetual trade, or other asset-affecting job before it is submitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Katrina-jpg/acp-job-submitter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, text] <br>
**Output Format:** [Markdown with command examples and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ACP agent wallet addresses, service names, requirements payload examples, job status commands, and pricing examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
