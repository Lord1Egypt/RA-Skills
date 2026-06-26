## Description: <br>
Mirror congressional stock trades with automated broker execution and risk management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mainfraame](https://clawhub.ai/user/mainfraame) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure and run an OpenClaw agent that monitors congressional trade disclosures and can execute scaled E*TRADE brokerage orders with configured risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place unattended real-money trades through E*TRADE. <br>
Mitigation: Start with sandbox credentials, review trading limits before production use, and leave daemon, cron, or systemd automation disabled unless unattended trading is intentional. <br>
Risk: Broker credentials and OAuth tokens may be stored with weak local persistence controls. <br>
Mitigation: Protect ~/.clawback and the SQLite database, avoid production keys until reviewed, and remove or ignore debug authentication scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mainfraame/clawback) <br>
- [E*TRADE Developer Portal](https://developer.etrade.com) <br>
- [House Clerk Disclosures](https://disclosures-clerk.house.gov) <br>
- [Senate eFD Search](https://efdsearch.senate.gov) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt for broker credentials, account settings, notification settings, and trading mode.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact package metadata lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
