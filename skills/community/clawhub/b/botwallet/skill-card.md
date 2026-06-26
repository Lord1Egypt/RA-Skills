## Description: <br>
Botwallet guides an agent through using the Botwallet CLI to create and manage a real USDC wallet on Solana, make payments, create paylinks, request funds, withdraw funds, and access paid APIs within owner-defined guard rails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasrazunnaiyyer](https://clawhub.ai/user/kasrazunnaiyyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use this skill to let an AI agent operate Botwallet's CLI for USDC payments, invoicing, fund requests, withdrawals, and x402 paid API access under human-controlled limits and approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to operate a real USDC wallet and initiate payments, withdrawals, invoices, and x402 purchases. <br>
Mitigation: Use a dedicated low-balance wallet with strict per-transaction limits, daily limits, merchant allowlists, and owner approval requirements for withdrawals and unfamiliar services. <br>
Risk: The local wallet seed share and API key can authorize sensitive wallet operations if exposed. <br>
Mitigation: Treat ~/.botwallet/seeds/* and BOTWALLET_API_KEY as secrets; do not print, log, commit, or share them. <br>
Risk: Automatic invoice and payment flows can move money or request money in ways the owner did not intend. <br>
Mitigation: Require explicit owner confirmation before any payment, withdrawal, paylink, invoice, or x402 purchase, and preview or probe prices before confirming. <br>
Risk: Unread wallet events can include approval outcomes or funded requests that trigger follow-up financial actions. <br>
Mitigation: Review and act on actionable events before marking the event queue as read. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kasrazunnaiyyer/botwallet) <br>
- [Botwallet website](https://botwallet.co) <br>
- [Botwallet dashboard](https://app.botwallet.co) <br>
- [Botwallet CLI source](https://github.com/botwallet-co/agent-cli) <br>
- [Botwallet docs](https://docs.botwallet.co) <br>
- [Botwallet CLI npm package](https://www.npmjs.com/package/@botwallet/agent-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill assumes shell and network access and treats Botwallet CLI responses as JSON by default.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
