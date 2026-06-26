## Description: <br>
Monitors competitors across pricing, social media, online reviews, and product changes - distills everything into a concise weekly briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcvanstad](https://clawhub.ai/user/marcvanstad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business teams, founders, agencies, and analysts use this skill to monitor competitor pricing, social activity, reviews, product changes, news, and hiring signals, then turn those signals into alerts and weekly intelligence briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may monitor sites or platforms where scraping or automated collection is not permitted. <br>
Mitigation: Install only for targets the user is allowed to monitor, and review each site's terms and platform access requirements before enabling collectors. <br>
Risk: Reports and alerts can expose sensitive competitive strategy or collected third-party data through Slack, email, Telegram, archived files, or screenshots. <br>
Mitigation: Prefer file-only delivery until report contents are reviewed, use private channels, and reduce or purge archived raw data and screenshots when they are no longer needed. <br>
Risk: Webhook and API credentials used for delivery or data access may be exposed or overprivileged. <br>
Mitigation: Use dedicated low-privilege webhook and API credentials, avoid sharing them in repositories, and rotate them if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcvanstad/competitive-intelligence-agent) <br>
- [README](README.md) <br>
- [Scraping configuration](reference/config/scraping.yaml) <br>
- [Delivery configuration](reference/config/delivery.yaml) <br>
- [Weekly report template](reference/templates/weekly_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and alerts with inline shell commands and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate weekly briefings, targeted reports, real-time alerts, CSV or JSON exports, archived raw data, and screenshots depending on configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
