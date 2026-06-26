## Description: <br>
Generates actionable content ideas by aggregating trends from RSS feeds, Reddit, Hacker News, X/Twitter, and web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DimitriPantzos](https://clawhub.ai/user/DimitriPantzos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content marketers, founders, and social media teams use this skill to monitor public trend sources and turn relevant discussions into content ideas, hooks, angles, formats, and content-calendar inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trend research may summarize public web, RSS, or social sources and can include sensitive brand details if the user provides them. <br>
Mitigation: Keep secrets and sensitive brand material out of prompts and configuration, and review generated summaries before publishing. <br>
Risk: Recurring daily or weekly workflows can create idea files automatically. <br>
Mitigation: Confirm the schedule and output folder before enabling recurring runs, and review generated files before use. <br>
Risk: Results can depend on separate RSS, social-media, or web-search tools. <br>
Mitigation: Review and configure those dependent tools separately before relying on their results. <br>


## Reference(s): <br>
- [Content Ideas on ClawHub](https://clawhub.ai/DimitriPantzos/content-ideas) <br>
- [Hacker News RSS](https://news.ycombinator.com/rss) <br>
- [HNRSS Ask HN feed](https://hnrss.org/ask) <br>
- [Reddit r/Entrepreneur RSS](https://www.reddit.com/r/Entrepreneur/.rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown content idea lists with optional JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save scheduled daily or weekly idea files under content-ideas/ when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
