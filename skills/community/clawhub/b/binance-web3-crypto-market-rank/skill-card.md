## Description: <br>
Provides Binance Web3 crypto market leaderboards for social hype, trending and searched tokens, Binance Alpha and tokenized stocks, smart-money inflows, Pulse meme tokens, and trader PnL rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to answer crypto ranking questions by calling Binance Web3 leaderboards for tokens, public wallet activity, and trader performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to web3.binance.com and returns crypto token and public wallet leaderboard data. <br>
Mitigation: Use it for intended Binance Web3 crypto ranking questions and review returned public market data before relying on it. <br>
Risk: The skill may be an inappropriate default source for generic, non-crypto, or traditional market ranking questions. <br>
Mitigation: Use another source unless the user specifically asks for Binance Web3 or crypto market rankings. <br>


## Reference(s): <br>
- [CLI Reference](references/cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI calls return JSON from public Binance Web3 endpoints; some numeric market fields may be string-encoded.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence; skill frontmatter reports 3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
