## Description: <br>
Use the Nutshell (cashu) CLI to manage Cashu ecash wallets, send and receive tokens, and pay Bitcoin Lightning invoices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1denvalu3](https://clawhub.ai/user/a1denvalu3) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a Cashu wallet through the Nutshell CLI, including checking balances, sending and receiving ecash tokens, paying Lightning invoices, and handling Cashu 402 payment requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad no-confirmation authority to spend, pay, burn, claim, or retry paid Cashu and Lightning actions. <br>
Mitigation: Use a dedicated low-balance wallet and trusted mint, and require the agent to show the amount, recipient or endpoint, mint, and payment request before any send, pay, burn, LNURL, or 402-payment action. <br>


## Reference(s): <br>
- [Cashu ClawHub release page](https://clawhub.ai/a1denvalu3/cashu) <br>
- [Nutshell project repository](https://github.com/cashubtc/nutshell) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the cashu CLI plus CASHU_DIR and MINT_URL or MINT_HOST environment configuration.] <br>

## Skill Version(s): <br>
0.19.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
