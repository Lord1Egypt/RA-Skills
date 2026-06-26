## Description: <br>
Clawdit-lender helps an agent operate as an autonomous peer-to-peer crypto lender by evaluating loan requests, ERC-8004 reputation, and revenue history before setting loan amounts and terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NatX223](https://clawhub.ai/user/NatX223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to configure an autonomous lending agent that registers a smart wallet, evaluates borrower agents, disburses USDT loans on Sepolia, tracks loan status, and collects repayments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can move funds autonomously through lending and repayment operations. <br>
Mitigation: Use only testnet funds or funds the operator can afford to lose, and require explicit per-loan or capped policy approval before any disbursement. <br>
Risk: Persistent credentials and token allowances could allow unintended transactions. <br>
Mitigation: Store agentCode only in a real secret store, avoid unlimited token approvals, and keep a clear process to pause automation and revoke credentials or allowances. <br>
Risk: The artifact does not provide enough user controls or risk disclosure for autonomous crypto lending. <br>
Mitigation: Review the skill before installing and add operator-facing controls for loan limits, risk level, approval policy, and emergency shutdown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NatX223/clawdit-lender) <br>
- [Publisher profile](https://clawhub.ai/user/NatX223) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, API request examples, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides API calls for registration, balance checks, loan selection, disbursement, repayment collection, and history review.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
