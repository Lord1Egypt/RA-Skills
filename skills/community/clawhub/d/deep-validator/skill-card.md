## Description: <br>
Validates email addresses, URLs, domains, and bulk lists with live DNS, DNSBL, disposable-domain, HTTP reachability, redirect tracing, and risk checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vannelier](https://clawhub.ai/user/vannelier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to verify emails, URLs, domains, and contact lists before sending messages, following links, importing records, or running automated validation pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted service can receive emails, URLs, domains, and uploaded files for validation. <br>
Mitigation: Send only data the user is authorized to share with the third-party operator, and avoid confidential contact lists unless third-party processing is approved. <br>
Risk: Paid validation, bulk, file, async, and webhook workflows can incur charges through wallet or payment infrastructure. <br>
Mitigation: Use the free quote flow first and require explicit approval before confirming paid, bulk, file, async, or webhook requests. <br>
Risk: Secret-bearing URLs, internal hosts, and private network addresses may expose sensitive strings to the hosted operator before validation completes. <br>
Mitigation: Do not submit URLs containing tokens, passwords, API keys, internal hostnames, private IPs, or cloud metadata addresses. <br>


## Reference(s): <br>
- [Deep Validator ClawHub Page](https://clawhub.ai/vannelier/deep-validator) <br>
- [Hosted Deep Validator Endpoint](https://deep-validator-production.up.railway.app) <br>
- [Deep Validator Source Code](https://github.com/nathanleclaire/Agent_Validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [JSON validation results and Markdown usage guidance with curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include cost quotes, payment challenges, recommended actions, confidence scores, status details, redirect chains, and risk flags.] <br>

## Skill Version(s): <br>
2.5.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
