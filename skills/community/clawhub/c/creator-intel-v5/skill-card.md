## Description: <br>
Creator Intel V5 helps agents gather and summarize engineer-focused technology intelligence from GitHub, arXiv-style technical sources, hardware communities, and Chinese RSS feeds while filtering business-oriented coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uuoov](https://clawhub.ai/user/uuoov) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and technical researchers use this skill to generate concise daily briefs on open-source projects, architecture and algorithm developments, and niche hardware while de-emphasizing financing and PR coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships with and uses a hardcoded Tavily API key. <br>
Mitigation: Remove the embedded key, rotate it, and load Tavily credentials from user-controlled configuration before running the skill. <br>
Risk: The documented run and cron commands do not match the shipped script name. <br>
Mitigation: Verify and correct the exact command path before manual execution or scheduled delivery. <br>
Risk: The Feishu cron setup can run automatically after installation. <br>
Mitigation: Do not enable the scheduled job until the command has been verified and the operator knows how to disable it. <br>
Risk: History retention behavior may differ from the documented retention limit. <br>
Mitigation: Enforce the documented retention limit or update the documentation so users understand stored history behavior. <br>


## Reference(s): <br>
- [Creator Intel V5 on ClawHub](https://clawhub.ai/uuoov/creator-intel-v5) <br>
- [Tavily Search API](https://api.tavily.com/search) <br>
- [Jiqizhixin RSS](https://www.jiqizhixin.com/rss) <br>
- [QbitAI Feed](https://www.qbitai.com/feed) <br>
- [OSChina News RSS](https://www.oschina.net/news/rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted technology brief with dated sections, linked items, and concise Chinese summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads RSS feeds and Tavily search results, keeps URL history for de-duplication, and requires user-controlled Tavily credentials before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
