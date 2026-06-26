## Description: <br>
Crypto Alert helps an agent check public cryptocurrency prices, 24-hour changes, and simple surge or drop alerts using Binance market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dolphins1123](https://clawhub.ai/user/dolphins1123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current prices and 24-hour movement for supported cryptocurrencies, then present simple alerts when a coin rises or falls sharply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coin lookup requests are sent to Binance for public market data. <br>
Mitigation: Use the skill only when external Binance API requests are acceptable for the deployment environment. <br>
Risk: The artifact instructs users to install the unpinned Python requests package. <br>
Mitigation: Pin and review dependencies in the deployment environment before running the script. <br>
Risk: Server security evidence notes a stale marketplace summary. <br>
Mitigation: Rely on the included README and SKILL.md behavior description rather than the stale listing summary. <br>


## Reference(s): <br>
- [Crypto Alert ClawHub page](https://clawhub.ai/dolphins1123/crypto-alert) <br>
- [Binance API](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style text with command examples and price summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs public market prices, 24-hour percent changes, and simple alert labels for supported cryptocurrency symbols.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
