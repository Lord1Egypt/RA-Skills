## Description: <br>
每日财经早报：A股行情 + RSS新闻聚合，自动生成Markdown简报 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[answeryl](https://clawhub.ai/user/answeryl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance-news users and agents use this skill to collect A-share index data and China News Service RSS items, classify them, and produce a daily Markdown morning brief with optional WeChat delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact references scripts/morning_briefing.py, but that script is not included in the package. <br>
Mitigation: Confirm or add the script before running the manual or scheduled commands. <br>
Risk: The skill can write briefing archives to a local default folder. <br>
Mitigation: Review the output directory before execution and write only to approved locations. <br>
Risk: Optional WeChat delivery may distribute finance-news summaries to a channel. <br>
Mitigation: Enable scheduled delivery only for appropriate channels and review summaries for accuracy and audience suitability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/answeryl/cn-market-briefing) <br>
- [Skill homepage](https://clawhub.com/skills/morning-briefing) <br>
- [China News Service RSS](https://www.chinanews.com.cn/rss/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown briefing with shell and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a full local archive and a condensed WeChat push; the artifact notes a default archive path of ~/Desktop/早间新闻/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
