## Description: <br>
Fetches real-time meme-token and market-topic rankings from Binance Web3 for Solana and BSC launchpad activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexploarer](https://clawhub.ai/user/dexploarer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current meme-token launches, migration stages, and hot market topics for Solana and BSC. It is intended for market-data lookup and summarization, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live third-party market data may be incomplete, delayed, volatile, or unsuitable as trading advice. <br>
Mitigation: Treat outputs as informational market data, verify important results against primary sources, and avoid presenting results as investment recommendations. <br>
Risk: The artifact contains strong run-now wording that could encourage network lookups when the user only wants general discussion. <br>
Mitigation: Invoke the scripts only when the user asks for current meme-token or topic rankings; otherwise answer from the documentation without live calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dexploarer/binance-meme-rush) <br>
- [Binance Web3 Meme Rush rank API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list/ai) <br>
- [Binance Web3 Topic Rush rank API](https://web3.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list/ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [JSON returned by shell scripts, typically summarized as Markdown prose by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Binance Web3 network calls and accepts chain, stage, sort, and limit arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
