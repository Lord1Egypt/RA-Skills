## Description: <br>
Query DexScreener market data for token prices, pools, profiles, trends, and related crypto-market research through a Node.js CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuefer3](https://clawhub.ai/user/zuefer3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to look up DexScreener token, pair, pool, profile, transaction, advertising, and memecoin-category data for trading research and market monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an unpinned third-party npm package globally on first use, causing persistent changes to the Node/npm environment. <br>
Mitigation: Verify the package name and publisher, consider installing a pinned version yourself, and approve global installation only in an environment where persistent npm changes are acceptable. <br>
Risk: The skill is intended for crypto market-data lookup and may surface volatile or incomplete market information. <br>
Mitigation: Treat outputs as research data, cross-check important values against authoritative sources, and avoid using the skill output as standalone financial advice. <br>


## Reference(s): <br>
- [Dexscreener CLI ClawHub release](https://clawhub.ai/zuefer3/dexscreener-cli) <br>
- [Dexscreener CLI GitHub repository](https://github.com/Kilincarslan-Enterprises/dexscreener-cli) <br>
- [NPM package @kilincarslan-enterprises/dexscreener-cli](https://www.npmjs.com/package/@kilincarslan-enterprises/dexscreener-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and parsed JSON or table output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI returns JSON by default and can return human-readable tables when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
