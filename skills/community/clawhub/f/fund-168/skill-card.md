## Description: <br>
Monitors selected mutual funds and ETFs, calculates support and resistance levels, tracks alerts and holdings, and helps configure scheduled notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hustjim2026](https://clawhub.ai/user/hustjim2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors and operators use this skill to maintain a fund watchlist, calculate technical thresholds, schedule monitoring jobs, export backups, and receive fund movement notifications through configured channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled configuration includes a preconfigured Feishu webhook that could send fund reports to an unknown destination. <br>
Mitigation: Remove the bundled Feishu webhook from data/config.json and data/push_channels.json before use, then configure only notification destinations controlled by the user. <br>
Risk: Fund reports, holdings, cost basis, share counts, exports, and notification messages may expose sensitive personal financial information. <br>
Mitigation: Confirm where reports will be sent and how exported files will be stored before entering holdings data or enabling scheduled notifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hustjim2026/fund-168) <br>
- [Publisher profile](https://clawhub.ai/user/hustjim2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local watchlist, holdings, alert, push-channel, log, CSV, or XLSX files when the included monitoring script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
