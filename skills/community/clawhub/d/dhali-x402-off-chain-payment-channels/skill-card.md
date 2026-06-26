## Description: <br>
Manage Dhali assets and x402 payments for high-frequency, low-latency applications with minimal on-chain fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[desimmons](https://clawhub.ai/user/desimmons) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up Dhali-backed x402 payment flows for paid APIs, including provider resource servers and consumer payment signatures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment examples include automatic funding and paid-request flows without explicit spending limits. <br>
Mitigation: Use dedicated low-balance test wallets and require explicit user approval plus a spending cap before any deposit, asset update, or paid request. <br>
Risk: The skill depends on external SDKs and a facilitator endpoint for payment handling. <br>
Mitigation: Pin and verify SDK dependencies, confirm the exact network and facilitator endpoint, and review the full flow before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/desimmons/dhali-x402-off-chain-payment-channels) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, JavaScript, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment-channel setup guidance, provider resource-server examples, and consumer payment-signature examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
