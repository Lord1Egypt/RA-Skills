## Description: <br>
Collects scheduled finance news, market index, sector, and limit-up stock data and provides NocoDB import and browser tab cleanup workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoovaycn](https://clawhub.ai/user/hoovaycn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure recurring finance-data scraping jobs, import collected JSON records into NocoDB, and manage browser tabs used by the scraping workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The NocoDB import script contains a fixed external database URL, table ID, and real-looking token and may send local finance records to that destination. <br>
Mitigation: Remove hardcoded credentials and destination identifiers, rotate any exposed token, and load a least-privilege token and table IDs from a local secret or environment variable before running. <br>
Risk: The browser cleanup script closes non-Eastmoney tabs and extra Eastmoney tabs, which can disrupt unrelated browser work if run in a shared profile. <br>
Mitigation: Run cleanup only in an isolated browser profile or change the script to close only tabs created by this skill. <br>
Risk: Cron examples can repeatedly trigger scraping, importing, and tab cleanup jobs without further review. <br>
Mitigation: Review each cron schedule and target configuration before enabling recurring jobs, especially database destinations and browser profile scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoovaycn/finance-data-scraper) <br>
- [NocoDB configuration example](config-examples/nocodb-config.example.json) <br>
- [Cron configuration examples](config-examples/cron-configs/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown instructions with JSON configuration examples and Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recurring job examples, NocoDB import behavior, and local browser tab cleanup behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
