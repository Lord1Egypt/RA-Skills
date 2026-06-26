## Description: <br>
Add funds to the wallet. Use when you or the user want to fund, deposit, top up, load, add funds, onramp, buy crypto, or get tokens into the wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Wallet users use this skill when they need agent guidance for funding a Finance District wallet by web onramp or direct transfer. It helps check authentication, retrieve the correct wallet address for a chain, explain funding options, and verify balances after funding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto transfers can be irreversible if the user sends funds to the wrong chain, token, or address. <br>
Mitigation: Confirm the exact chain, token, and wallet address before funding, and use a small test transfer for first-time deposits. <br>
Risk: The skill depends on the Finance District fdx CLI for wallet status and address lookup. <br>
Mitigation: Install and use the skill only when the Finance District fdx CLI is trusted and authenticated for the intended wallet. <br>


## Reference(s): <br>
- [Fund Wallet on ClawHub](https://clawhub.ai/rachidjarray-hk-qa-fdt/fund-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance requires user confirmation before external funding actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
