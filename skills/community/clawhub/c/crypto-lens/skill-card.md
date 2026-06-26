## Description: <br>
CryptoLens provides paid cryptocurrency comparison, technical charting, and AI-style market analysis for selected crypto assets using Hyperliquid and CoinGecko market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Godofbush](https://clawhub.ai/user/Godofbush) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to compare two to five cryptocurrencies, generate single-asset technical analysis charts, and receive scored market analysis with chart output. The skill requires a BNB Chain billing wallet or user ID for SkillPay charging before each command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The paid SkillPay flow sends the user's billing wallet or user ID to SkillPay before command execution. <br>
Mitigation: Use only when the user understands the paid flow and has provided the billing identifier they want associated with charges. <br>
Risk: Server security evidence reports contradictory pricing evidence for the compare command. <br>
Mitigation: Verify the actual SkillPay charge for compare before use, especially before running comparisons repeatedly. <br>
Risk: Market-data queries are sent to third-party providers. <br>
Mitigation: Avoid submitting sensitive portfolio context beyond the coin symbols and duration needed for the requested analysis. <br>


## Reference(s): <br>
- [CryptoLens on ClawHub](https://clawhub.ai/Godofbush/crypto-lens) <br>
- [Publisher Profile](https://clawhub.ai/user/Godofbush) <br>
- [SkillPay](https://skillpay.me) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={currency}) <br>
- [Hyperliquid Info API](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Text, Guidance] <br>
**Output Format:** [JSON containing text_plain and optional chart_path, with PNG chart files referenced for media display] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create PNG chart files under /tmp and may return a SkillPay payment_url when billing balance is insufficient.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
