## Description:

Daily Intel Report collects AI industry news and procurement notices, filters them by recency and keywords, and formats a Chinese daily report for Feishu or email delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to gather public AI news and Zhejiang procurement information, then produce a concise Chinese daily intelligence report for scheduled or on-demand delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public news and procurement data, including procurement items from an HTTP source that could be inaccurate if intercepted.

Mitigation: Treat collected procurement items as untrusted public data and verify important notices against the official source before making decisions.

Risk: Scheduled delivery to Feishu or email could send reports to unintended recipients if notification settings are misconfigured.

Mitigation: Review recipient and SMTP or Feishu configuration before enabling scheduled delivery.

## Reference(s):

- [Data Sources](references/data-sources.md)
- [AIBase News](https://www.aibase.com/news)
- [IT Home AI Channel](https://www.ithome.com/tags/AI/)
- [Zhejiang Government Procurement Search](http://www.ccgp-zhejiang.gov.cn/portal/searchHome)
- [ClawHub Skill Page](https://clawhub.ai/lgugeng/skills/daily-intel-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese daily report text or Markdown with source links and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include procurement titles, buyers, regions, bid opening dates, and links from public sources.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
