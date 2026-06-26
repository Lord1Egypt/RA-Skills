## Description: <br>
A FluxA Agent Wallet skill that enables agents to request budgets, sign x402 payments, and call paid endpoints autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpppppp7](https://clawhub.ai/user/cpppppp7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to request user-approved FluxA wallet budgets, obtain x402 payment signatures, and call paid HTTP endpoints with an X-PAYMENT header. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates payment authority and can spend from a FluxA wallet budget. <br>
Mitigation: Use small task-specific budgets, confirm the endpoint and payment payload before spending, and communicate the maximum requested budget to the user before creating a mandate. <br>
Risk: The security evidence notes extra wallet-transfer capability and persistent wallet credentials that are not clearly scoped in the user-facing instructions. <br>
Mitigation: Install only when the publisher and FluxA are trusted, avoid payout commands unless an explicit transfer is intended, and protect or remove ~/.fluxa-ai-wallet-mcp/config.json when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cpppppp7/fluxa-x402-payment) <br>
- [FluxA Agent ID API](https://agentid.fluxapay.xyz) <br>
- [FluxA Wallet API](https://walletapi.fluxapay.xyz) <br>
- [FluxA Wallet App](https://wallet.fluxapay.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces FluxA CLI command guidance for mandate creation, mandate status checks, x402 payment signing, and paid endpoint calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
