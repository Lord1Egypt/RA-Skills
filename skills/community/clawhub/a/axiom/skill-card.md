## Description: <br>
Use Axiom Wallet via MCP to manage payment methods, review account activity, and complete user-requested purchases through Axiom's server-managed browser checkout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axiom-wallet](https://clawhub.ai/user/axiom-wallet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to connect to Axiom Wallet, check saved payment-method metadata, review recent transactions, and start user-requested purchases that require Axiom approval flows before completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A connected agent can read wallet transaction and payment-method metadata. <br>
Mitigation: Install only when the user intends to let an agent use Axiom Wallet, use OAuth approval, and avoid exposing tokens, cookies, browser state, or OAuth authorize URLs. <br>
Risk: The skill can start purchases through Axiom Wallet. <br>
Mitigation: Require clear user intent, verify the payment method before purchase, wait for Axiom approval links, and never claim success until purchase status returns completed. <br>


## Reference(s): <br>
- [Axiom ClawHub listing](https://clawhub.ai/axiom-wallet/axiom) <br>
- [Authentication guide](references/authentication.md) <br>
- [Axiom MCP endpoint](https://mcp.useaxiom.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter >=0.8.0 and OAuth approval before account or purchase tools can be used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
