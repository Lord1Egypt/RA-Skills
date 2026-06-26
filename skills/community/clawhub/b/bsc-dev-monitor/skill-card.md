## Description: <br>
Monitors specified BSC wallet addresses for token transfers and returns detection details, webhook-ready notifications, monitoring history, and billing status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mybusd](https://clawhub.ai/user/mybusd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External crypto traders, BSC wallet watchers, and developers use this skill to monitor dev-wallet token transfer activity, receive webhook alerts, and review detection history before deciding whether to investigate a token further. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded payment and ClawHub credentials may be real and could be misused. <br>
Mitigation: Remove embedded secrets, rotate exposed keys and passwords, and require environment-based secret configuration before installation or deployment. <br>
Risk: Deployment scripts can publish uploads or perform release actions. <br>
Mitigation: Do not run deployment scripts during review or installation; inspect release commands and require an authenticated publisher-controlled deployment process. <br>
Risk: Billing behavior is described inconsistently across per-call and per-detection modes. <br>
Mitigation: Clarify the exact billing mode, price, and charge trigger in the public listing and runtime output before users initiate monitoring. <br>
Risk: Webhook notifications and monitoring history may expose wallet activity or transaction details. <br>
Mitigation: Document webhook data handling, retention limits, and endpoint validation controls; use HTTPS webhooks and avoid storing unnecessary monitoring history. <br>
Risk: Detected tokens may still be unsafe or misleading investment signals. <br>
Mitigation: Present detections as monitoring output only and require independent review of token contracts, liquidity, and honeypot risk before trading. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mybusd/bsc-dev-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/mybusd) <br>
- [BSC Documentation](https://www.binance.org/en/smart-chain) <br>
- [SkillPay](https://skillpay.me) <br>
- [SkillPay Documentation](https://docs.skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and Markdown usage guidance with JavaScript and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns monitor status, detected token metadata, transaction hashes, webhook payloads, billing fields, and history records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
