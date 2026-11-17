## Description:

Monitors bidding opportunities in the lithium battery, energy storage, and assembly equipment sectors, tracks four named competitors, and produces weekly reports with optional email delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardcoder849](https://clawhub.ai/user/richardcoder849)

### License/Terms of Use:

MIT-0

## Use Case:

Business development, sales, and market intelligence teams use this skill to collect bid leads from battery and energy-storage markets, enrich them with company and budget context, prioritize follow-up, and generate weekly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping bid sources with disabled TLS certificate verification can expose fetched business data to interception or tampering.

Mitigation: Restore normal HTTPS verification before operational use and restrict fetching to approved public bidding domains.

Risk: Generated reports and local history files may contain business intelligence gathered from bid sources.

Mitigation: Review retention, access control, and sharing rules for report and history outputs before enabling scheduled collection.

Risk: SMTP delivery can send generated reports externally when credentials and recipients are configured.

Mitigation: Keep email sending as an explicit opt-in step, protect SMTP credentials, and verify the recipient list before production use.

Risk: Spreadsheet output can carry untrusted scraped content into downstream analysis workflows.

Mitigation: Sanitize Excel output before sharing or opening it in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/richardcoder849/skills/bid-watcher)
- [BeiJiXing Energy Network](https://www.bjx.com.cn)
- [Energy Storage China Network](https://www.escn.com.cn)
- [China Power Equipment Management Network](https://www.cpem.org.cn)
- [China Energy Network](https://www.cnenergy.com)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown reports, Excel spreadsheets, JSON data files, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can maintain local report history and send generated reports by SMTP when email settings are configured.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
