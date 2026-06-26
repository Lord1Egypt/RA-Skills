## Description: <br>
Tracks crypto wallet addresses locally and retrieves current USD prices for common assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill as a simple local notebook for wallet addresses and a command-line price checker for common crypto assets. It is not a full portfolio valuation, profit calculator, or automated reporting system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses are saved locally in ~/.crypto-portfolio.json. <br>
Mitigation: Use only public wallet addresses you are comfortable storing on the local machine and remove the local JSON file when it is no longer needed. <br>
Risk: Price checks call CoinGecko and may be unavailable, delayed, or insufficient for precise accounting. <br>
Mitigation: Treat returned prices as convenience estimates and verify values with an authoritative source before making financial or tax decisions. <br>
Risk: The artifact presents broader portfolio and profit-reporting claims than the implementation supports. <br>
Mitigation: Use it as a wallet-address notebook and basic price checker rather than a complete holdings monitor or profit calculator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/crypto-holdings-monitor) <br>
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON storage for wallet addresses and performs network price lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
