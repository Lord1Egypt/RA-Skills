## Description: <br>
Automatically generates daily fund reports with configured fund holdings, valuation changes, net asset values, and financial news, with output as a Telegram message and Word document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiashuoji838-afk](https://clawhub.ai/user/jiashuoji838-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors or operators use this skill to produce a daily report for configured fund codes, including fund NAV, valuation changes, trading-day status, financial news, and delivery through Telegram and a Word document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded Telegram credentials and chat destination may send fund reports to an unintended external recipient. <br>
Mitigation: Remove and rotate the embedded Telegram bot token, replace the chat ID with a verified destination, and disable Telegram delivery until configuration is reviewed. <br>
Risk: The skill invokes a hardcoded local news-market script path for news aggregation. <br>
Mitigation: Verify or replace the script path before enabling news aggregation, and run only trusted local scripts. <br>
Risk: Scheduled execution can repeatedly send reports or write files after installation. <br>
Mitigation: Create scheduled tasks only after configuration is fixed, destinations are verified, and dependencies are pinned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiashuoji838-afk/funds-agent) <br>
- [Fund valuation data endpoint](http://fundgz.1234567.com.cn/js/{fund_code}.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Configuration guidance, Shell commands] <br>
**Output Format:** [Telegram-ready text plus a Word document, with Markdown documentation and shell command examples for setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided fund codes, Telegram settings if delivery is enabled, network access to fund/news sources, and a configured local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
