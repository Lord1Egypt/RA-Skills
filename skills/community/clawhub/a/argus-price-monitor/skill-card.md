## Description: <br>
Monitors product prices across e-commerce sites daily, detects price drops, and emails a formatted Excel report automatically every morning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, ecommerce, and pricing teams use this skill to monitor configured product URLs, compare current prices with prior runs, and receive daily Excel reports by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled scraping and automatic email delivery can affect external sites or send reports before configuration is reviewed. <br>
Mitigation: Install only for intended monitoring, verify monitored URLs and recipients, and require confirmation before the first email send. <br>
Risk: SMTP credentials and report recipients could expose business data if over-privileged or misconfigured. <br>
Mitigation: Use a dedicated SMTP account or app password, allowlist recipients, and keep secrets in the platform secret store. <br>
Risk: Local raw data and generated reports may accumulate pricing history beyond the intended retention period. <br>
Mitigation: Set retention limits for raw scrape data and report files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neo1307/argus-price-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, configuration] <br>
**Output Format:** [Excel workbook, email with attachment, CSV raw data, and console summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured product URLs, SMTP settings, and a Chromium-capable Selenium runtime.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
