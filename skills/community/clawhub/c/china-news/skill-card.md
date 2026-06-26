## Description: <br>
China News aggregates recent Chinese news from sources such as Sina, Sohu, NetEase, and Tencent through RSS or browser automation and generates categorized news reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather recent Chinese news from public sources, categorize items by topic, and produce a dated news report. It supports RSS-first collection and optional browser-based collection when an OpenClaw browser tool is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public news and RSS sites. <br>
Mitigation: Use it only where network access to those sources is allowed, or disable network access in restricted environments. <br>
Risk: The skill writes a dated Markdown report in the current workspace or OPENCLAW_WORKSPACE. <br>
Mitigation: Review the destination before running and delete generated reports when they are no longer needed. <br>
Risk: News site structures, RSS feeds, and source availability may change over time. <br>
Mitigation: Review the generated report for completeness and source freshness before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/china-news) <br>
- [Publisher profile](https://clawhub.ai/user/tobewin) <br>
- [Sina News](https://news.sina.com.cn) <br>
- [Sohu News RSS](https://news.sohu.com/rss/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report and inline Python or JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a dated news_YYYYMMDD.md report in the current workspace or OPENCLAW_WORKSPACE.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
