## Description: <br>
Provides a CLI-backed agent workflow for querying live meme-token launchpad lifecycle feeds and AI-detected market hot topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external crypto-analysis agents use this skill to query Binance Web3 public endpoints for new, finalizing, and migrated meme tokens and AI-ranked hot narratives across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary and guidance in server evidence refer to a different fuel-price and EV-charger helper, so they may not describe this skill's actual behavior. <br>
Mitigation: Treat the server-resolved security verdict as authoritative for this card, but have a reviewer confirm that the evidence bundle matches the Binance Meme Rush artifact before release. <br>
Risk: The artifact uses live crypto market data and includes capability tags for wallet and sensitive-credential contexts. <br>
Mitigation: Use the skill for informational market discovery only, avoid providing wallet credentials to the skill, and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binance-skills-hub/binance-web3-meme-rush) <br>
- [Publisher profile](https://clawhub.ai/user/binance-skills-hub) <br>
- [CLI reference](references/cli.md) <br>
- [Binance Web3 meme-rush endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list/ai) <br>
- [Binance Web3 topic-rush endpoint](https://web3.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list/ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent in selecting subcommands, filters, and display handling for JSON API responses.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
