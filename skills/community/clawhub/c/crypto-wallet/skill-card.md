## Description: <br>
Multi-chain cryptocurrency wallet management. Check balances, send tokens, view transaction history across Ethereum, Solana, Bitcoin and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nvmmonkey](https://clawhub.ai/user/nvmmonkey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to ask an agent for cryptocurrency wallet balance checks, transaction history, portfolio summaries, token price lookups, and transfer preparation across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to handle irreversible cryptocurrency transfers without enough detail about wallet access and transaction safeguards. <br>
Mitigation: Review before installing and require the user to approve each transaction outside the agent after seeing the exact chain, token, amount, recipient, fees, and contract action. <br>
Risk: Exposure of seed phrases or raw private keys could compromise wallet funds. <br>
Mitigation: Do not provide seed phrases or raw private keys to the agent or skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text responses with wallet-management guidance and command-oriented steps when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq according to ClawHub metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
