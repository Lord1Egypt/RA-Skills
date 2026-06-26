## Description: <br>
Fetch top news from Baidu, Google, and other sources daily. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to fetch a concise daily list of trending news topics from Baidu and Google Trends through a Python script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Baidu and Google Trends. <br>
Mitigation: Run it in an isolated environment and allow outbound network access only to expected news and trends endpoints. <br>
Risk: Dependencies are listed without pinned versions. <br>
Mitigation: Install in a virtual environment or container and pin dependency versions before production use. <br>
Risk: The printed Beijing-time label may use the runtime host timezone. <br>
Mitigation: Confirm the runtime timezone or update the script to use an explicit Asia/Shanghai timezone. <br>
Risk: Command execution could be misused for file access, credential exposure, or repeated polling. <br>
Mitigation: Execute only daily_news.py, install only from requirements.txt, sanitize error output, and require user direction before any retry. <br>


## Reference(s): <br>
- [Daily News Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/daily-news-hardened) <br>
- [Faberlens Daily News Safety Evaluation](https://faberlens.ai/explore/daily-news) <br>
- [Baidu Realtime Hot Search](https://top.baidu.com/board?tab=realtime) <br>
- [Google Trends Daily Search RSS](https://trends.google.com/trends/trendingsearches/daily/rss?geo=US) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text news list with Markdown setup and execution instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs the Python news script at most once per user request; results depend on upstream Baidu and Google Trends availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
