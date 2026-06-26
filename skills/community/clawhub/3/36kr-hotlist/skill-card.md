## Description: <br>
获取36氪官方24小时热榜文章数据. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[36kr-com](https://clawhub.ai/user/36kr-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and summarize the official 36kr 24-hour hot-list articles for a given date, including ranks, titles, authors, publish times, summaries, and article links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the public 36kr/OpenClaw CDN to fetch hot-list results. <br>
Mitigation: Use it only when retrieving public 36kr hot-list data is expected and acceptable for the agent environment. <br>
Risk: The skill presents recommendations for related 36kr skills after showing results. <br>
Mitigation: Install or invoke additional recommended skills only when the user wants them and trusts their source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/36kr-com/36kr-hotlist) <br>
- [API reference](api-reference.md) <br>
- [Usage examples](examples.md) <br>
- [36kr hot-list API endpoint template](https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json) <br>
- [36kr full hot-list page](https://36kr.com/hot-list/catalog?channel=skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown article list with optional JSON, CSV, Python, or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public 36kr hot-list data; each daily response contains up to 15 articles and may fall back to recent prior dates when the current date is unavailable.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
