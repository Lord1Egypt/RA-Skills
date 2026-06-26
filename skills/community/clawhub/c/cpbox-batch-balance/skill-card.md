## Description: <br>
Guide users on how to use the Batch EVM Address Balance Query API (/api/x402/batch-balance) for batch balance queries, multicall balance lookups, and calls to the x402-protected balance endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare batch EVM balance requests against CPBox's x402-protected endpoint and understand the request parameters, payment flow, and response shape. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-signed x402 payments may be made automatically by helper clients without clear confirmation or spending-limit instructions. <br>
Mitigation: Use a dedicated low-balance wallet, verify payment requirements and amount before each request, and avoid using a primary private key in code or chat. <br>
Risk: Using external payment packages with wallet credentials can expose users to package or configuration risk. <br>
Mitigation: Pin and review the external payment package before use and keep wallet credentials outside shared prompts, logs, and examples. <br>


## Reference(s): <br>
- [CPBox API provider](https://www.cpbox.io) <br>
- [Batch balance endpoint](https://www.cpbox.io/api/x402/batch-balance) <br>
- [CPPay facilitator](https://www.cppay.finance) <br>
- [x402-payment wallet configuration](https://github.com/springmint/x402-payment#wallet-configuration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API call examples] <br>
**Output Format:** [Markdown with bash, TypeScript, Go, cURL, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes request and response examples plus x402 payment-flow guidance for a paid API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
