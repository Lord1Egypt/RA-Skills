## Description:

Finance Data Scraper helps agents set up scheduled workflows for scraping Eastmoney finance news, market index data, sector leaders, and limit-up stocks into NocoDB, with browser tab cleanup support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoovaycn](https://clawhub.ai/user/hoovaycn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure recurring finance data scraping jobs, deduplicate records, and import market monitoring data into NocoDB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary reports a hard-coded remote database credential.

Mitigation: Rotate or remove the embedded NocoDB token and require users to provide their own destination configuration before execution.

Risk: The browser cleanup workflow can close non-Eastmoney tabs in the active OpenClaw browser session.

Mitigation: Run browser automation in an isolated browser profile or change cleanup behavior to close only tabs created by this skill.

Risk: Scheduled import jobs send scraped finance records to the configured NocoDB destination.

Mitigation: Verify the base URL, table IDs, and token scope before enabling cron jobs or automated imports.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, Python scripts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided NocoDB destination settings and table IDs for normal use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
