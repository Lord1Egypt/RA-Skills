## Description: <br>
Send USDC on Base, read balances, and pay x402-protected resources using a Coinbase CDP server wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ales375](https://clawhub.ai/user/ales375) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent check wallet balances, send USDC on Base, inspect recent transfers, and pay x402-protected resources through a Coinbase CDP server wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move USDC and make paid x402 web requests from the configured Coinbase CDP wallet. <br>
Mitigation: Use a dedicated low-balance wallet, test with base-sepolia first, and require explicit approval or CDP policy limits before allowing autonomous payments. <br>
Risk: The skill does not include built-in spending, recipient, domain, or network limits. <br>
Mitigation: Restrict approved recipients and x402 domains outside the skill, and enforce hard limits through Coinbase CDP policy controls where available. <br>
Risk: CDP API credentials and the wallet secret authorize wallet operations. <br>
Mitigation: Store the credentials only in isolated secret storage, avoid sharing funded wallets across agents or tenants, and rotate the wallet secret if compromise is suspected. <br>


## Reference(s): <br>
- [CDP Wallet ClawHub Page](https://clawhub.ai/ales375/cdp-wallet) <br>
- [Publisher Profile](https://clawhub.ai/user/ales375) <br>
- [Skill Homepage](https://github.com/Ales375/openclaw-cdp-wallet-skill) <br>
- [Coinbase CDP Server Wallets v2 Documentation](https://docs.cdp.coinbase.com/server-wallets/v2/introduction/welcome) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [Single-line JSON from CLI subcommands, with setup and invocation guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI outputs include wallet addresses, balances, transaction hashes, transfer history, x402 settlement details, and structured error objects; secrets are expected to remain in environment variables.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
