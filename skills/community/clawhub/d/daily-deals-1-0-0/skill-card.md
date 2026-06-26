## Description: <br>
Generates concise daily shopping-deal reports from configured deal sources and can deliver them through console, webhook, or Feishu channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gf1023456](https://clawhub.ai/user/gf1023456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and deal-tracking operators use this skill to convert scraped or saved shopping-source data into scheduled daily deal reports and notifications. <br>

### Deployment Geography for Use: <br>
Global, with source coverage centered on Chinese shopping platforms. <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Feishu scripts include hardcoded credentials and a fixed recipient. <br>
Mitigation: Remove embedded credentials and recipient IDs, rotate exposed credentials, and require users to provide delivery settings through local configuration or environment variables. <br>
Risk: Scheduled or automatic notification runs can send generated reports to unintended destinations. <br>
Mitigation: Run report generation manually and inspect the output before enabling cron or push commands; keep default delivery console-only until destinations are explicitly configured. <br>
Risk: Deal reports are generated from scraped or saved source data and may be stale or inaccurate. <br>
Mitigation: Verify price, availability, seller, and promotion terms at the linked source before purchasing or acting on a report. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gf1023456/daily-deals-1-0-0) <br>
- [SMZDM deal source](https://www.smzdm.com/) <br>
- [Shihuo deal source](https://www.shihuo.cn/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like plain text reports with product titles, prices, source links, statistics, and delivery instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local daily-report.txt file and send report text to configured channels; Feishu delivery requires credential and recipient review before use.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
