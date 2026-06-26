## Description: <br>
Earn yield on USDC by supplying to the Moonwell Flagship USDC vault on Base. Use when depositing USDC, withdrawing from the vault, checking position/APY, or generating yield reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sergey1997](https://clawhub.ai/user/Sergey1997) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use Gekko Yield to manage USDC deposits, withdrawals, position checks, APY reporting, and reward compounding for the Moonwell Flagship USDC vault on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This is a hot-wallet DeFi skill that can approve tokens and submit live Base transactions. <br>
Mitigation: Use a dedicated wallet with limited USDC, WELL, MORPHO, and ETH, and review every transaction before execution. <br>
Risk: Auto-compounding swaps reward tokens through Odos and can deposit available USDC back into the vault. <br>
Mitigation: Review the Odos-based transaction before execution and do not keep idle USDC in the wallet before running compound unless it should be deposited. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sergey1997/gekko-yield) <br>
- [Base RPC endpoint](https://mainnet.base.org) <br>
- [Odos quote API](https://api.odos.xyz/sor/quote/v2) <br>
- [Odos assemble API](https://api.odos.xyz/sor/assemble) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; script outputs include plain text, JSON, and Telegram/Discord-formatted reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, USDC on Base, ETH on Base for gas, and a private key supplied at runtime through an environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
