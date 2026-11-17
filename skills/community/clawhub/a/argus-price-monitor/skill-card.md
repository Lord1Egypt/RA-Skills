## Description:

Monitors product prices across e-commerce sites daily, detects price drops, and emails a formatted Excel report automatically every morning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external business users, and developers use this skill to monitor configured e-commerce product URLs, compare daily prices, and receive an Excel report by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses configured websites with weak browser isolation.

Mitigation: Run it in a restricted container or dedicated account, remove --no-sandbox where possible, and restrict outbound network access to approved domains.

Risk: The skill builds and emails Excel reports from untrusted web data.

Mitigation: Harden the Excel export against formula injection before emailing reports and review SMTP recipients before deployment.

Risk: Untrusted or overly broad product URL lists can expand browsing and scraping exposure.

Mitigation: Use only trusted product URLs and maintain an allowlist for monitored domains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neo1307/skills/argus-price-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/neo1307)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Excel workbook, email message, and console summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates dated raw CSV and Excel report files, then emails the Excel report when SMTP settings are configured.]

## Skill Version(s):

1.0.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
