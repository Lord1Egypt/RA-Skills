## Description: <br>
AI DevBlog Factory gathers GitHub Trending and technical news, analyzes trends, generates structured developer reports, and can publish them to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to monitor GitHub Trending and technical news sources, turn the results into AI-assisted trend analysis and markdown articles, and optionally publish the output to Feishu for team knowledge sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated content or Feishu publishing could accidentally share information with the wrong workspace or audience. <br>
Mitigation: Run with draft mode first, verify the destination folder and Feishu permissions, and enable cron or notifications only after confirming the generated content is safe to share. <br>
Risk: Dependent skills perform the scraping and Feishu write operations, so their behavior affects the release risk. <br>
Mitigation: Review the dependent skills before installing or scheduling this workflow. <br>
Risk: GitHub and RSS sources can be rate-limited or unavailable, which may produce incomplete reports. <br>
Mitigation: Use conservative schedules, review empty or sparse results, and adjust source configuration before relying on generated reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zlszhonglongshen/ai-devblog-factory) <br>
- [dev.to RSS Feed](https://dev.to/feed) <br>
- [Hacker News RSS Feed](https://news.ycombinator.com/rss) <br>
- [TechCrunch RSS Feed](https://www.techcrunch.com/feed/) <br>
- [O'Reilly Radar RSS Feed](https://feeds.feedburner.com/oreilly/radar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Configuration] <br>
**Output Format:** [Structured JSON analysis, markdown article content, and Feishu document metadata when publishing is enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports language, time range, RSS sources, Feishu folder, article title, draft mode, and notification settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
