## Description: <br>
Uses Akshare market data to build and cross-check current A-share, ChiNext, B-share, and Sci-Tech Innovation Board stock lists, then separates actively trading stocks from stocks not present in real-time quote feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch Chinese equity list data, compare it with real-time Akshare quote endpoints, and produce CSV/JSON outputs that distinguish currently trading stocks from stocks missing in spot-market feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags under-scoped persistent retry instructions that could create scheduled background agent work. <br>
Mitigation: Do not create cron jobs or scheduled agent turns unless the exact task, duration, output path, logs, and removal command are shown and approved first. <br>
Risk: The skill recommends VPN use when Akshare or Eastmoney quote endpoints are blocked. <br>
Mitigation: Use VPN guidance only when it complies with the user's organization and network policy. <br>
Risk: Market-data endpoint failures or partial coverage can produce incomplete trading and non-trading lists. <br>
Mitigation: Review generated CSV and JSON outputs before relying on them, especially when B-share or Sci-Tech Innovation Board endpoints fail. <br>


## Reference(s): <br>
- [Current Akshare List on ClawHub](https://clawhub.ai/ugpoor/current-akshare-list) <br>
- [Publisher profile: ugpoor](https://clawhub.ai/user/ugpoor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated data files are CSV and JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes stock-list and spot-market comparison outputs such as stocklist.csv, stocklist_intrading.csv, notspot.csv, and temporary Akshare JSON files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
