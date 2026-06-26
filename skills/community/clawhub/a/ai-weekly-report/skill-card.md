## Description: <br>
Generates a structured AI weekly news report from listed public AI news sources for a user-specified date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongyusheng](https://clawhub.ai/user/dongyusheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to gather recent AI news over a requested date range and turn the findings into a concise weekly report grouped by event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report depends on public news pages that may be unavailable, stale, or inaccessible for the requested date range. <br>
Mitigation: Record inaccessible articles, cite the source links that were actually accessed, and verify important items before relying on the report. <br>
Risk: The skill may save a date-based Markdown report in the current directory, which can conflict with an existing file using the same name. <br>
Mitigation: Check for an existing file with the same date-based name before saving or run the skill in a dedicated working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongyusheng/ai-weekly-report) <br>
- [Daily AI News](https://ai-bot.cn/daily-ai-news/) <br>
- [Aiera](https://aiera.com.cn/) <br>
- [GeekPark](https://www.geekpark.net/) <br>
- [QbitAI](https://www.qbitai.com/) <br>
- [RadarAI](https://radarai.top/) <br>
- [Wanxiang AI Lab](https://yunyinghui.feishu.cn/wiki/HNyWwm4BJie3fDkwg11chMTbngb) <br>
- [Jiqizhixin](https://www.jiqizhixin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Structured Markdown report with event titles, event dates, summaries, and original source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided date range no longer than one month and may save a date-based Markdown file in the current directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
