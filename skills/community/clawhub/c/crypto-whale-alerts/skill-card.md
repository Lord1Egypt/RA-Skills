## Description: <br>
Tracks large on-chain cryptocurrency transactions and whale wallet movements to generate configurable alert text, summaries, and watchlist output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent workflows use this skill to run local crypto whale transaction scans, view summaries, inspect watched wallet labels, and configure alert thresholds. Outputs should be reviewed as market-monitoring signals rather than trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local mock transaction data and should not be treated as live market intelligence or trading advice. <br>
Mitigation: Use it as a local starting point until live data integrations are added and independently tested. <br>
Risk: Security evidence reports misleading inflow/outflow trading-label behavior. <br>
Mitigation: Correct and test the classification logic before relying on the alerts in production or decision-support workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/crypto-whale-alerts) <br>
- [Etherscan Transaction Link Template](https://etherscan.io/tx/{tx_hash}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and Markdown documentation with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WHALE_MIN_USD and WHALE_COOLDOWN environment variables for threshold and cooldown configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
