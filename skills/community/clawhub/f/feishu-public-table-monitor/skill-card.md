## Description: <br>
Monitors publicly accessible Feishu/Lark wiki or document tables for version, model, rate, and price changes, then outputs Telegram/Markdown-ready change notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quqi1599](https://clawhub.ai/user/quqi1599) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor public Feishu/Lark price, model, rate, or product tables and produce change notifications suitable for Telegram or Markdown delivery. It can also guide cron-style scheduled monitoring with local JSON baselines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches a user-supplied Feishu/Lark URL and stores local JSON baselines for comparison. <br>
Mitigation: Use only non-sensitive public URLs and set --state-dir when you need to control where snapshots are stored. <br>
Risk: A Feishu/Lark page structure change or an incorrect section title can cause the script to miss or misread the intended table. <br>
Mitigation: Run with --print-snapshot first to confirm the parsed table before scheduling recurring checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quqi1599/feishu-public-table-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notifications, JSON snapshots, and shell command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The monitoring script prints NO_REPLY when no change is detected and INIT_ONLY when it creates the initial baseline.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
