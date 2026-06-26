## Description: <br>
Make paid requests to x402-enabled APIs using USDC on Base when the user explicitly asks to call a paid API, make an x402 payment, pay for a request, or fetch from a paid endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to inspect and make paid x402 API requests with USDC on Base after intentionally invoking a paid-service workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 API calls can spend USDC and send request data to arbitrary third-party endpoints without a final price or data confirmation. <br>
Mitigation: Before each payment, require the agent to show the endpoint, HTTP method, request body and headers, exact price, and a conservative `--max-amount`. <br>
Risk: Wallet or token credentials can authorize spending from the configured account. <br>
Mitigation: Use a limited wallet or token containing only funds you are willing to spend, and verify authentication and balance before making paid calls. <br>
Risk: Unvalidated URL, method, JSON body, headers, query parameters, or max-amount values can create unsafe or unintended requests. <br>
Mitigation: Validate HTTPS URLs, allowed HTTP methods, JSON inputs, and positive integer max amounts before constructing the Agnic CLI command. <br>


## Reference(s): <br>
- [x402 Protocol Reference](reference/x402-protocol.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/agnicpay-prog/agnicpay-pay-for-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON command output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute paid x402 API calls through the Agnic CLI when the user intentionally requests payment.] <br>

## Skill Version(s): <br>
2.0.2 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
