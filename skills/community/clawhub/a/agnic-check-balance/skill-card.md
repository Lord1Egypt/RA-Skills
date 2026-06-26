## Description: <br>
Check USDC balance across supported Base and Solana networks, including balance checks, available USDC, funds views, and wallet balance verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check USDC wallet balances across Base and Solana networks through the Agnic CLI. It is useful when a user needs to confirm available funds, inspect balances by network, or verify wallet status before another wallet-related action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, balances, and authentication status are private financial information. <br>
Mitigation: Treat CLI output and tokens as sensitive, avoid pasting tokens into chat or shell history, and prefer environment variables for AGNIC_TOKEN. <br>
Risk: The skill depends on the Agnic CLI/package and the wallet account it connects to. <br>
Mitigation: Install and run it only when the Agnic CLI/package and connected wallet account are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agnicpay-prog/agnic-check-balance) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose wallet addresses, balances, network names, and authentication status from Agnic CLI output.] <br>

## Skill Version(s): <br>
2.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
