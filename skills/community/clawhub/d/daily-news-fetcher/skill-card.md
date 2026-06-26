## Description: <br>
Fetch and summarize daily news headlines from mainstream news sources, returning five top headlines with brief summaries in a structured format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve a concise daily headline digest from public RSS feeds when asked for current news summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external BBC, Xinhua, and NYTimes RSS feeds when invoked, so output may fail, change, or reflect third-party feed content. <br>
Mitigation: Use it for lightweight headline summaries, disclose the feed sources to users, and avoid treating the output as a complete or authoritative news ranking. <br>
Risk: The artifact documentation claims Reuters support, translation, and hot-topic ranking, but release security guidance characterizes the implementation as a basic feed formatter. <br>
Mitigation: Represent the skill as a public RSS headline formatter unless the publisher updates the documentation and code to support the broader claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/daily-news-fetcher) <br>
- [BBC News RSS feed](https://feeds.bbci.co.uk/news/rss.xml) <br>
- [Xinhua English News RSS feed](http://www.xinhuanet.com/english/news_english.xml) <br>
- [NYTimes World RSS feed](https://rss.nytimes.com/services/xml/rss/nyt/World.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Structured text digest with headline, source, and summary fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces up to five news items; output depends on public RSS feed availability and feed contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
