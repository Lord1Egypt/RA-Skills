## Description: <br>
Track cryptocurrency markets in real time, including crypto prices, market sentiment, DeFi TVL, trending coins, meme coins, RSI indicators, moving averages, yield comparisons, and Ethereum gas fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve cryptocurrency market data and educational crypto-market guidance through shell-based commands and supporting Chinese-language reference material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is shell-based and contacts public cryptocurrency market-data APIs. <br>
Mitigation: Install only in environments where outbound calls to those APIs are acceptable, and review the shell scripts before execution. <br>
Risk: The release includes under-disclosed local financial logging and persistence for portfolio, alert, and history data. <br>
Mitigation: Use a dedicated data directory, avoid entering sensitive financial information, and review or disable local logging behavior before relying on the tool. <br>
Risk: The included trading strategy material can be mistaken for financial advice. <br>
Mitigation: Treat strategy and signal content as educational material and require independent review before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/bytesagain-crypto-tracker-cn) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>
- [DefiLlama API](https://api.llama.fi) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market data, educational guidance, local portfolio or alert records, and command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
