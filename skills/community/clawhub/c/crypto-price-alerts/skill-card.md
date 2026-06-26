## Description: <br>
Set and manage cryptocurrency price alerts and receive notifications when watched pairs reach target prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and crypto market watchers use this skill to create, list, remove, and check local price alerts for cryptocurrency pairs without continuously monitoring charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watched trading pairs and target prices are stored in a local JSON file. <br>
Mitigation: Install only where local workspace files are acceptable for this information, and remove the stored alerts when they are no longer needed. <br>
Risk: Alerts and notification claims may not be reliable enough for time-sensitive trading decisions without testing. <br>
Mitigation: Test alert checks and notification delivery before relying on the skill, and verify market prices independently before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/crypto-price-alerts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON status messages and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores alert definitions locally and queries Binance through ccxt when checking alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
