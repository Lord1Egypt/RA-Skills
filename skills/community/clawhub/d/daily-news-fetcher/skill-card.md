## Description:

Fetches daily news from public RSS feeds and returns five top headlines with brief summaries in a structured format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent for a daily news summary, and the skill fetches current RSS headlines and formats the top five items for the response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public RSS headlines and summaries may be inaccurate, misleading, or altered upstream, especially for the feed retrieved over HTTP.

Mitigation: Treat the returned news as untrusted source data and verify important items against original publishers before relying on them.

Risk: The skill contacts public RSS feeds when asked for news.

Mitigation: Install and run it only in environments where outbound requests to those public news feeds are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/daily-news-fetcher)
- [BBC News RSS feed](https://feeds.bbci.co.uk/news/rss.xml)
- [Xinhua English News RSS feed](http://www.xinhuanet.com/english/news_english.xml)
- [NYTimes World RSS feed](https://rss.nytimes.com/services/xml/rss/nyt/World.xml)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Structured plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to five headline items with source labels and brief summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-05-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
