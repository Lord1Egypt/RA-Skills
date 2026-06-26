## Description: <br>
Interact with the Hyperscaled funded trading platform to check trading accounts, view positions and orders, submit or cancel trades, review balances and rules, browse miners, check registration or KYC status, and manage Hyperscaled configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taoshidev1](https://clawhub.ai/user/taoshidev1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to operate Hyperscaled funded-account workflows through the Hyperscaled CLI or SDK. It supports account monitoring, position and order review, trade validation and submission, funded-account registration, KYC checks, payouts, and risk-limit review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit trades, cancel orders, purchase funded accounts, start KYC, and update configuration. <br>
Mitigation: Require explicit user confirmation before any trade, cancel-all, funded-account purchase, KYC start, or configuration update. <br>
Risk: Trading actions can breach account rules or risk limits. <br>
Mitigation: Validate trades before submission and highlight drawdown, account type, and leverage warnings before proceeding. <br>
Risk: Private keys and wallet-related secrets may be exposed if pasted into chat or command arguments. <br>
Mitigation: Do not paste private keys into chat or command arguments; use environment-variable based handling when a private key is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/taoshidev1/funded-account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include readable account, position, order, payout, rule, miner, KYC, and risk summaries.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
