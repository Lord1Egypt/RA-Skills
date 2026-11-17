## Description:

Generates China A-share pre-market, intraday, and post-market review reports using market data from Tushare, AKShare, Sina Finance, and fallback web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare recurring China A-share market briefings, intraday snapshots, and post-market review reports. It is intended for market summarization and strategy framing, not individual stock recommendations or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring report pushes may be enabled by default and sent to linked messaging destinations.

Mitigation: Install only when recurring financial reports are desired, review each destination, and disable or require approval for scheduled pushes before use.

Risk: The Tushare token flow may expose credentials because the documented API endpoint uses HTTP.

Mitigation: Do not store a valuable Tushare token for this version unless the endpoint is changed to HTTPS and the credential-handling flow is reviewed.

Risk: Generated reports may appear current even when some data is missing or replaced by hard-coded claims.

Mitigation: Treat reports as unverified, check source data before acting, and remove or clearly label hard-coded market claims in production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/china-a-stocks-daily-review)
- [Tushare Pro API](http://api.tushare.pro)
- [Tushare token page](https://tushare.pro/user/token)
- [README.md](artifact/README.md)
- [report_template.md](artifact/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Python scripts, and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated report files and an intermediate JSON data file during local execution.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
