## Description: <br>
中国新闻聚合(免费版) helps agents fetch public Chinese news RSS feeds, classify items by topic, and generate structured news briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to gather headlines from public Chinese RSS feeds, classify them into basic news categories, and produce daily Markdown briefs in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt the agent to run Python commands and install the requests package. <br>
Mitigation: Review generated commands before execution and run them in a controlled workspace. <br>
Risk: The skill fetches public RSS feeds and may contact a callback URL if one is supplied. <br>
Mitigation: Allow only expected feed domains and provide a callback URL only when outbound contact to that endpoint is intended. <br>
Risk: The skill can write generated news briefs or cache data into the working directory or configured output directory. <br>
Mitigation: Set an explicit output directory and inspect generated files before using or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/china-news-tool-free) <br>
- [Sina domestic news RSS feed](https://rss.sina.com.cn/news/china/roll.xml) <br>
- [Sohu news RSS feed](https://news.sohu.com/rss/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefs, Python snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated news briefs or cache files to the working directory or configured output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
