## Description: <br>
Monitor cryptocurrency prices and trigger alerts when thresholds are hit, with support for BTC, ETH, SOL, and other CoinGecko-listed assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongtaop1-sys](https://clawhub.ai/user/yongtaop1-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure cryptocurrency price checks, compare current prices against thresholds, and receive console or Telegram alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts CoinGecko and can send alert messages to Telegram when credentials are configured. <br>
Mitigation: Review network destinations before use and keep Telegram credentials out of shared files and repositories. <br>
Risk: Some documented percent-based alert modes are not implemented in the bundled script. <br>
Mitigation: Use above or below threshold alerts by default, or add and test percent-based condition handling before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yongtaop1-sys/crypto-price-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/yongtaop1-sys) <br>
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price) <br>
- [Telegram sendMessage endpoint](https://api.telegram.org/bot{bot_token}/sendMessage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, Python code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write triggered alert records or logs when the bundled script is run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
