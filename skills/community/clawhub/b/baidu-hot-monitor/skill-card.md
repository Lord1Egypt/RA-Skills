## Description: <br>
百度热榜监控 | Baidu Hot Topics Monitor. 获取百度热搜榜、搜索趋势、关键词热度 | Get Baidu trending searches, trends, keyword popularity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-1106](https://clawhub.ai/user/noah-1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Baidu hot-search topics, monitor keyword popularity, save local trend history, query collected records, and generate an HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent local SQLite databases, logs, and HTML reports containing retained monitoring history. <br>
Mitigation: Use it only in workspaces where retained local Baidu trend data is acceptable, and review or delete the data directory when the history is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noah-1106/baidu-hot-monitor) <br>
- [Baidu realtime hot topics API](https://top.baidu.com/api/board?platform=wise&tab=realtime) <br>
- [Baidu Top](https://top.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples, JSON examples, Python scripts, SQLite data, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python 3, fetches public Baidu trend data, and may create persistent local SQLite databases, logs, and HTML reports under the skill data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
