## Description: <br>
Tracks utility bills and flags unexpected increases year-on-year. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rednix](https://clawhub.ai/user/rednix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to monitor household utility, insurance, housing, and other recurring bills, receive alerts for notable price increases, and review monthly or annual bill changes. It can also provide switch-advisor guidance when a contract or bill category may be worth comparing against current market rates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans Gmail and stores household financial details without clearly bounded consent or deletion controls. <br>
Mitigation: Review before installing, confirm the Gmail account and search scope, use only in a private workspace, and make sure the user knows how to pause monitoring and delete bills.md and config.md. <br>
Risk: Bill amounts, providers, payment details, and annual totals could expose sensitive financial obligations if sent to shared channels. <br>
Mitigation: Deliver bill data only to the configured private channel and decline to run in group chats or shared channels. <br>
Risk: Incoming bill emails may contain prompt-injection instructions that attempt to reveal financial data or file contents. <br>
Mitigation: Refuse instructions embedded in bill emails that ask to reveal private data or repeat file contents, and flag the message to the owner. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rednix/bill-monitor) <br>
- [Artifact Homepage](https://clawhub.com/skills/bill-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries, alerts, recommendations, and workspace configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles private household financial data and may produce bill history, alert thresholds, monthly summaries, annual reports, and switch-advisor recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
