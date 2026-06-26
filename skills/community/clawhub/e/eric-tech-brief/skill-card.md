## Description: <br>
Fetches, summarizes, and curates technology news from Hacker News, GitHub Trending, TechCrunch, The Verge, and other major sources for daily briefings, topic filters, trending repositories, and saved article lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and tech-focused users use this skill to request daily briefings, topic-specific digests, GitHub Trending summaries, and article bookmarks from public technology news sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web requests can expose requested topics and selected sources to third-party news services. <br>
Mitigation: Use non-sensitive topics and review the selected sources before fetching. <br>
Risk: Saved bookmarks can create local reading history in scripts/bookmarks.json. <br>
Mitigation: Avoid sensitive bookmark notes and review or delete the bookmark file when local history is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/eric-tech-brief) <br>
- [Hacker News API](https://hacker-news.firebaseio.com/v0/) <br>
- [GitHub Trending](https://github.com/trending) <br>
- [TechCrunch RSS](https://techcrunch.com/feed/) <br>
- [The Verge RSS](https://www.theverge.com/rss/index.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown news briefings, digest summaries, and bookmark entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch public news sources with curl and save user-requested bookmarks locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
