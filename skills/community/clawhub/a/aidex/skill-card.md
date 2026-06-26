## Description: <br>
Aidex lets an agent swap tokens on Ethereum through the AIDEX aggregator, search tokens, check exchange rates, view balances, execute swaps, and keep private-key transaction signing local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almiashev](https://clawhub.ai/user/almiashev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Aidex to let an OpenClaw agent search Ethereum tokens, quote swaps, check balances, execute user-approved swaps, and verify transaction status while signing locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent raw wallet-signing authority for irreversible Ethereum swaps and approvals. <br>
Mitigation: Use only a dedicated trading wallet with limited funds, require explicit confirmation unless an automated strategy is deliberately configured, and review token addresses, amount, slippage, deadline, gas, approvals, and transaction hashes before relying on a swap. <br>
Risk: A compromised host or exposed AIDEX_PRIVATE_KEY can permanently compromise wallet funds. <br>
Mitigation: Never use a main wallet key, avoid passing private keys on command lines, prefer local keyring storage where available, and restrict access to the machine running the agent. <br>
Risk: Automated trading can execute unwanted swaps if limits and retry behavior are not controlled. <br>
Mitigation: Set strict strategy limits, stop on errors or reverted transactions, avoid automatic retries, and verify each swap with the status script and final balance checks. <br>


## Reference(s): <br>
- [Aidex ClawHub Page](https://clawhub.ai/almiashev/aidex) <br>
- [AIDEX Homepage](https://ai-dex.io/) <br>
- [AIDEX Security Model](artifact/references/security.md) <br>
- [AIDEX Script Reference](artifact/references/scripts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with JSON outputs from local Node.js scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only token, rate, balance, and status operations can run without a private key; swap execution requires AIDEX_PRIVATE_KEY and produces on-chain Ethereum transaction hashes.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
