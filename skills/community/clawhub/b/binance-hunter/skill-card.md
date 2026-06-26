## Description: <br>
The Hunter: Professional Binance Trading Skill. Features AI market analysis, auto-risk calculation, and 125x leverage support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TetrAVAD](https://clawhub.ai/user/TetrAVAD) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to analyze Binance market data, prepare spot and futures trading commands, and configure Binance API credentials for account queries and order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Binance spot and futures orders, cancellations, and leverage changes. <br>
Mitigation: Use Binance testnet first and require explicit confirmation before every order, cancellation, or leverage change. <br>
Risk: Binance API credentials could expose account trading authority if over-scoped or poorly protected. <br>
Mitigation: Use a dedicated restricted API key, disable withdrawals, restrict by IP where possible, keep balances low, and protect the credential file. <br>
Risk: Leveraged trading can amplify losses, especially when using high leverage. <br>
Mitigation: Keep leverage low unless the user has deliberate experience and verify symbol, quantity, stop loss, and take profit settings before execution. <br>
Risk: The artifact includes a referral link that may benefit the publisher. <br>
Mitigation: Treat the referral link as self-serving but disclosed and avoid presenting it as neutral documentation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TetrAVAD/binance-hunter) <br>
- [Binance API Documentation](https://binance-docs.github.io/apidocs/) <br>
- [Binance Testnet](https://testnet.binance.vision/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON code blocks; the bundled analyzer emits JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, python3, and Python dependencies for market analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
