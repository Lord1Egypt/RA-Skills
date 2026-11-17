## Description:

Generates a structured weekly report of recent AI news from a fixed set of Chinese-language AI news sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongyusheng](https://clawhub.ai/user/dongyusheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and editors use this skill to gather AI news within a requested date range, merge duplicate event coverage across sources, and produce a concise weekly report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches content from external news sites, so source pages may be unavailable, stale, or inconsistent.

Mitigation: Use the requested date range, record inaccessible articles, and include only URLs that were actually accessed in the report.

Risk: The skill may create a Markdown report file in the current working directory.

Mitigation: Run it in a workspace where creating a report file is expected and review the generated filename and path.

Risk: A missing or overly broad date range can produce an unfocused or excessive report.

Mitigation: Require the user to provide a date range and enforce the documented maximum span of one month.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongyusheng/skills/ai-weekly-report)
- [Daily AI News](https://ai-bot.cn/daily-ai-news/)
- [Aiera](https://aiera.com.cn/)
- [GeekPark](https://www.geekpark.net/)
- [QbitAI](https://www.qbitai.com/)
- [RadarAI](https://radarai.top/)
- [Wanxiang AI Lab](https://yunyinghui.feishu.cn/wiki/HNyWwm4BJie3fDkwg11chMTbngb)
- [Jiqizhixin](https://www.jiqizhixin.com/)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown report or direct text response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a Markdown file in the current directory when file operations are available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
