## Description: <br>
查询CCF（中国计算机学会）近期学术会议、认证竞赛、活动日程等信息，支持按兴趣偏好筛选活动、判断报名状态，并为已结束活动检索数字图书馆视频和讲稿。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alucard118](https://clawhub.ai/user/alucard118) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up current CCF conferences, academic events, certifications, competitions, and related post-event resources. It is useful when the user needs a structured Markdown summary with dates, locations, registration status, official links, and optional personalized recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes recurring reminder automation for CCF news, events, certifications, and competitions. <br>
Mitigation: Review each proposed cron schedule, prompt text, and enabled state before approving persistent jobs; disable or remove jobs that are no longer needed. <br>
Risk: The Puppeteer helper can create or modify local browser configuration when invoked with the configuration option. <br>
Mitigation: Avoid the configuration helper unless local .env changes are acceptable, and review any generated browser path settings before use. <br>
Risk: Broad auto-triggers may activate the skill for general CCF-related conversations. <br>
Mitigation: Narrow or disable broad triggers if the deployment needs more explicit user intent before event lookup or automation guidance runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alucard118/ccf-events) <br>
- [CCF homepage](https://www.ccf.org.cn) <br>
- [CCF meeting system](https://conf.ccf.org.cn/conf/show.action?code=index) <br>
- [CCF digital library search](https://dl.ccf.org.cn/V2/toSearchList.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables with inline links and occasional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dated event tables, registration states, recommendation rationale, and links to CCF pages or digital library resources.] <br>

## Skill Version(s): <br>
1.1.421 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
