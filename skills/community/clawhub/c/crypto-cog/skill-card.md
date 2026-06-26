## Description: <br>
AI crypto research and analysis powered by CellCog. Token deep-dives, on-chain metrics, DeFi protocol breakdowns, wallet portfolio reviews, market sentiment, whitepaper analysis, smart contract evaluation. Comprehensive crypto intelligence from a single prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask CellCog for crypto research, including token analysis, DeFi protocol reviews, on-chain and market intelligence, portfolio strategy, and whitepaper or smart-contract due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be sent to CellCog and could expose sensitive crypto details if users include wallet addresses, exchange account identifiers, seed phrases, private keys, exact balances, or transaction histories. <br>
Mitigation: Share only the minimum data needed, use ranges or sample portfolios where possible, and never include seed phrases, private keys, or unnecessary account identifiers. <br>
Risk: The skill requires CELLCOG_API_KEY, which could be exposed if pasted into prompts or committed to files. <br>
Mitigation: Store the key in an environment variable or secret manager and keep it out of prompts, logs, and committed artifacts. <br>
Risk: Crypto research output can be incomplete, stale, or unsuitable as financial advice. <br>
Mitigation: Treat results as research support, verify on-chain and market data with primary sources, and apply independent review before making investment, tax, or regulatory decisions. <br>


## Reference(s): <br>
- [Crypto Cog on ClawHub](https://clawhub.ai/nitishgargiitd/crypto-cog) <br>
- [CellCog](https://cellcog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and optional report outputs such as HTML dashboards, PDF reports, XLSX spreadsheets, or Markdown analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the cellcog dependency, and CELLCOG_API_KEY; generated research should be verified against primary sources before financial decisions.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
