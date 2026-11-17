## Description:

百度热榜监控 | Baidu Hot Topics Monitor. 获取百度热搜榜、搜索趋势、关键词热度 | Get Baidu trending searches, trends, keyword popularity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch Baidu hot search topics, store collected results in a local SQLite database, query recent topics and category counts, and generate a local HTML visualization report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can render remote topic data unsafely when the report is opened or hosted.

Mitigation: Escape remote data and replace innerHTML-based rendering before using reports with untrusted data or publishing them.

Risk: The advertised trend, region, and keyword-monitoring scope is broader than the implemented scripts demonstrate.

Mitigation: Validate required analysis capabilities against the actual script outputs before relying on the skill for decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/noah-1106/skills/baidu-hot-monitor)
- [Baidu Hot Search API](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Baidu Top](https://top.baidu.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, HTML files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, plain-text query output, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; writes local SQLite data and an HTML report under data/ when the included scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
