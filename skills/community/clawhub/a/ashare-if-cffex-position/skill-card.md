## Description:

Downloads and parses CFFEX stock-index futures position-ranking XML for IF, IH, IC, and IM contracts, then produces Chinese-language position and net-change reports for CITIC Futures client accounts and the published top-20 market members.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangxingv5](https://clawhub.ai/user/fangxingv5)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and agents use this skill to fetch public CFFEX position-ranking data, calculate long, short, and net-position changes using the official varvolume field, and generate a local HTML report for review. It is intended for market-data reporting and research support, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded market data is not integrity-protected because the skill uses HTTP and disables TLS verification.

Mitigation: Treat reports as unauthenticated market data, verify important figures against CFFEX independently, and prefer a version that uses HTTPS with normal certificate validation when available.

Risk: Generated position reports may be misused as trading advice.

Mitigation: Use the report as research support only and keep the skill's investment-risk disclaimer visible in generated outputs.

Risk: The skill fetches public exchange XML and writes local cache and report files.

Mitigation: Invoke it explicitly in workspaces where local report and cache file creation is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangxingv5/skills/ashare-if-cffex-position)
- [CFFEX position ranking page](http://www.cffex.com.cn/cn/ccpm.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Chinese-language console summaries and a generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local cache files and a report named 股指期货持仓统计_YYYYMMDD.html in the current working directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
