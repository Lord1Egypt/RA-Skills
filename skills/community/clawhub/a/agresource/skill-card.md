## Description: <br>
Scrapes and summarizes AgResource grain newsletters with daily sales advice, price-impact sentiment analysis, trend tracking, and Telegram alerts on updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianppetty](https://clawhub.ai/user/brianppetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agricultural-market operators use this skill to automate collection of AgResource newsletters, summarize grain-market advice, track price-impact sentiment, and receive alerts when sales advice changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded AgResource credentials may be used unintentionally or expose an account. <br>
Mitigation: Remove and rotate embedded credentials before installation, and require user-supplied AGRESOURCE_EMAIL and AGRESOURCE_PASSWORD values. <br>
Risk: Paid newsletter-derived content and screenshots may be stored locally. <br>
Mitigation: Confirm access rights, storage location, and retention expectations before running the scraper or scheduled jobs. <br>
Risk: Scheduled runs and Telegram alerts may send information at the wrong time or to the wrong destination. <br>
Mitigation: Verify the cron schedule, newsletter type mapping, and Telegram destination before enabling automation. <br>
Risk: The Playwright dependency source may not match the installer's expectations. <br>
Mitigation: Verify the Playwright installation path and dependency source before executing the scraper. <br>


## Reference(s): <br>
- [ClawHub Agresource package](https://clawhub.ai/brianppetty/agresource) <br>
- [AgResource dashboard](https://agresource.com/dashboard/#/reports/daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown summaries, JSON sentiment history, Telegram alert text, and command-line invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AgResource credentials, Playwright, local file storage, and optional scheduled execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
