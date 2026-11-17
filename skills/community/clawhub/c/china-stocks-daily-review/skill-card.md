## Description:

Generates China A-share pre-market briefings, intraday snapshots, and post-market review reports using market data fallbacks across Tushare Pro, AKShare, and search-based sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate concise daily A-share market briefings, intraday checks, and post-market recaps. It is intended for market overview reporting, sentiment review, sector rotation tracking, and strategy-watch framing, not individualized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring delivery may send generated market reports to linked messaging channels by default.

Mitigation: Disable auto-push unless recurring delivery is explicitly desired, and verify the configured destination before enabling scheduled reports.

Risk: The skill can use a locally stored Tushare token and accesses the Tushare API over HTTP.

Mitigation: Avoid using a Tushare token until an HTTPS endpoint is available; if use is necessary, use an isolated environment and a low-privilege token.

Risk: Generated current-dated financial narratives may contain hard-coded or unverified claims.

Mitigation: Treat reports as informational only, verify market data and narrative claims against authoritative sources, and do not use the output as investment advice.

Risk: The Python scripts fetch external market data and require third-party packages.

Mitigation: Run dependencies in an isolated environment and review network access before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/china-stocks-daily-review)
- [Publisher profile](https://clawhub.ai/user/kooui)
- [Tushare Pro API endpoint](http://api.tushare.pro)
- [Tushare token page](https://tushare.pro/user/token)
- [Sina Finance quote endpoint](http://hq.sinajs.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-language Chinese/English market report text and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When scripts are run, the skill may save local report_YYYYMMDD_*.md files and a fetch_data.json intermediate file.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
