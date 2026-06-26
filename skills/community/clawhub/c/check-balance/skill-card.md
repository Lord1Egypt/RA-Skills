## Description: <br>
Check USDC balance across networks including Base and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and wallet users use this skill to check USDC balances across supported Base and Solana networks through the Agnic CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Agnic authentication credentials to check wallet balances. <br>
Mitigation: Keep `AGNIC_TOKEN` private, prefer environment variables over command-line token arguments, and avoid exposing command output that contains wallet details. <br>
Risk: Balance checks could be run for the wrong network or for unsupported wallet contexts. <br>
Mitigation: Confirm requests are for USDC wallets on supported Base or Solana networks before running the balance command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agnicpay-prog/check-balance) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Agnic CLI balance and status commands; balance output may include wallet addresses and network-specific USDC balances.] <br>

## Skill Version(s): <br>
2.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
