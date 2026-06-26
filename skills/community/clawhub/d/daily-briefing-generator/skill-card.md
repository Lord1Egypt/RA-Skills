## Description: <br>
每日简报生成器聚合多源资讯，并以结构化 Markdown 格式生成每日简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams and developers use this skill to generate concise daily briefings from topic keywords using Tavily search results. It is best suited for manual briefing generation until the advertised RSS and scheduled push workflows are supplied and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics and queries are sent to Tavily when the generator runs. <br>
Mitigation: Use a scoped Tavily API key and avoid confidential search topics unless sending them to Tavily is acceptable. <br>
Risk: The documentation advertises RSS ingestion and scheduled team push features that are not present in the reviewed artifact. <br>
Mitigation: Rely on the reviewed manual Tavily-based briefing workflow only; do not deploy RSS or scheduled push workflows until the missing files and credential handling are provided and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/daily-briefing-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TAVILY_API_KEY when Tavily search is available; can write the generated briefing to a file path supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
