## Description: <br>
Automatically generates daily fund reports with fund net value, estimated changes, data dates, and financial news, with optional Telegram delivery and Word document output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiashuoji838-afk](https://clawhub.ai/user/jiashuoji838-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual users or developers use this skill to generate scheduled daily fund summaries from configured fund codes, then receive the report as a Telegram message and a Word document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that this skill can send reports to a hardcoded Telegram recipient. <br>
Mitigation: Remove and rotate the embedded Telegram token, replace the chat ID with the intended destination, and confirm Telegram delivery is desired before running or scheduling the skill. <br>
Risk: The security scan reports a dependency on an unbundled local news-market script. <br>
Mitigation: Review, replace, or remove the external news script dependency so the report source and execution path are explicit in the target environment. <br>
Risk: The skill is intended for recurring scheduled execution and outbound report delivery. <br>
Mitigation: Review configuration, destination, and network behavior before enabling a task scheduler or cron job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiashuoji838-afk/fund-daily) <br>
- [天天基金网 fund data endpoint](http://fundgz.1234567.com.cn/js/{fund_code}.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Telegram message text and Word document file, with setup guidance and shell commands in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates scheduled or manually triggered reports for configured fund codes and can send outbound Telegram messages and documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
