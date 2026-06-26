## Description: <br>
Crypto Arbitrage Monitor monitors cryptocurrency price differences across supported exchanges, calculates fee-adjusted spreads, and sends Feishu or Telegram alerts for potential arbitrage opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OceanKing57](https://clawhub.ai/user/OceanKing57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to run a Python-based monitor for cross-exchange cryptocurrency spreads, review fee-adjusted opportunities, and receive alerts through configured Feishu or Telegram destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned or broadly pinned Python dependencies may change behavior over time. <br>
Mitigation: Pin or lock dependency versions before deployment and review package updates before applying them. <br>
Risk: Feishu or Telegram credentials and webhooks can expose alert channels if shared or committed. <br>
Mitigation: Keep credentials private, use only alert destinations you control, and rotate any token or webhook that may have been exposed. <br>
Risk: The monitor continuously polls exchange APIs until stopped, which can create operational load or rate-limit issues. <br>
Mitigation: Run it in a controlled environment, tune the polling interval, and stop the process when monitoring is no longer needed. <br>
Risk: Arbitrage alerts are informational and may not reflect executable profit after latency, liquidity, transfer time, or venue limits. <br>
Mitigation: Treat alerts as monitoring signals only and independently verify prices, fees, balances, liquidity, and execution constraints before trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OceanKing57/crypto-arb-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/OceanKing57) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled monitor also emits runtime log text and optional Feishu or Telegram alert messages when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
