## Description: <br>
Add money to the wallet through a Coinbase Onramp flow for USDC funding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to help fund a wallet with USDC, open the wallet companion funding interface, provide the wallet address for manual Base-network deposits, and check funding status or balance. <br>

### Deployment Geography for Use: <br>
Global, subject to Coinbase Onramp regional availability and payment-method support. <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens a financial funding flow and may be activated from insufficient-balance or onramp requests. <br>
Mitigation: Require explicit user confirmation before opening the funding interface or directing the user to purchase USDC. <br>
Risk: The security review flags `npx awal@latest` usage and wildcard Bash permissions around the wallet CLI. <br>
Mitigation: Review before installing, pin or justify the CLI version, and narrow allowed commands to exact funding, address, status, and balance checks where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xRAG/fund) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides wallet funding actions and balance checks; does not itself complete purchases.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
