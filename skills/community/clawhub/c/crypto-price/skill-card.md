## Description: <br>
Get cryptocurrency token price and generate candlestick charts via CoinGecko API or Hyperliquid API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evgyur](https://clawhub.ai/user/evgyur) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to fetch current cryptocurrency prices and generate candlestick charts for supported CoinGecko or Hyperliquid tokens. It is intended for market-data lookup and chart generation, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public CoinGecko or Hyperliquid APIs and depends on their availability, rate limits, and market-data accuracy. <br>
Mitigation: Use the output as informational market data, surface API errors clearly, and avoid presenting prices or charts as financial advice. <br>
Risk: The local Python script writes temporary cache and chart files under /tmp. <br>
Mitigation: Run it in an environment where temporary file writes are acceptable and clear generated files according to local retention needs. <br>
Risk: The dependency requirement allows a range of matplotlib versions, which can affect reproducibility. <br>
Mitigation: Pin dependencies in controlled deployments when reproducible installs or stable chart rendering are required. <br>


## Reference(s): <br>
- [Crypto Price on ClawHub](https://clawhub.ai/evgyur/crypto-price) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3/) <br>
- [Hyperliquid API](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files] <br>
**Output Format:** [JSON containing price fields, text_plain, and chart_path; agents may present text_plain with the generated PNG chart as media.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes temporary cache and chart files under /tmp; market data comes from public CoinGecko or Hyperliquid APIs.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
