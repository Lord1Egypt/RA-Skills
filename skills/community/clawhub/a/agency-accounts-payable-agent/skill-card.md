## Description: <br>
Accounts Payable Agent supports vendor and contractor payment workflows, payment-rail selection, idempotency checks, audit trails, and escalation for exceptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouqkt](https://clawhub.ai/user/zhouqkt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and operations teams use this skill to coordinate accounts-payable work such as vendor invoice payments, contractor payouts, recurring bill handling, payment-status reporting, and exception escalation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct real-money payments across fiat, crypto, stablecoin, and payment API rails. <br>
Mitigation: Install only where payment tools enforce approved vendors and accounts, allowlisted wallets and bank accounts, spend limits, and required approvals. <br>
Risk: Requests from other agents could cause duplicate, unauthorized, or incorrectly scoped payments if controls are weak. <br>
Mitigation: Require idempotency checks, per-payment or batch approval policies, audit logging, and human review for exceptions or limit breaches. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhouqkt/agency-accounts-payable-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown and structured payment-status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate externally constrained payment tool calls when integrated with financial systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
