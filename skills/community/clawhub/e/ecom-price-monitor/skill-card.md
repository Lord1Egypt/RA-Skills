## Description: <br>
Monitors competitor prices across cross-border e-commerce marketplaces, triggers price alerts, analyzes trends, and supports pricing decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guaguaren](https://clawhub.ai/user/guaguaren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers, pricing operators, and developers use this skill to configure product price monitoring, receive change alerts, review historical trends, export reports, and identify potential cross-market arbitrage opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace monitoring can violate platform terms or trigger rate limits when product URLs are checked too frequently. <br>
Mitigation: Review each marketplace's rules before use, configure a reasonable monitoring interval, and avoid high-frequency scraping. <br>
Risk: The skill may require API keys, SMTP credentials, webhook URLs, or 1688 cookies for platform access and notifications. <br>
Mitigation: Keep credentials out of prompts, logs, and source control, and enable email or webhook notifications only for trusted destinations. <br>
Risk: Price, inventory, and arbitrage outputs may be delayed, incomplete, or based on configured assumptions. <br>
Mitigation: Validate exported data and pricing recommendations against authoritative marketplace data before making business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guaguaren/ecom-price-monitor) <br>
- [Skill README](artifact/ecom-price-monitor/docs/README.md) <br>
- [Skill configuration](artifact/ecom-price-monitor/config/settings.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, YAML, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also guide JSON or spreadsheet-style export workflows for monitored price data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata, skill.json, configuration, and README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
