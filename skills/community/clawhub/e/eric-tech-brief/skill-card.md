## Description:

Fetches, summarizes, and curates technology news from public sources including Hacker News, GitHub Trending, TechCrunch, The Verge, and Ars Technica.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for daily technology briefings, topic-filtered news summaries, GitHub Trending repository summaries, markdown digests, and local article bookmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching public news sources can surface stale, duplicated, or low-quality third-party content.

Mitigation: Review summaries before relying on them, prefer source links for important claims, and respect the documented 10-minute cache guidance.

Risk: Using the save feature stores article details and optional notes or tags in a local bookmarks file.

Mitigation: Avoid saving sensitive notes, and review or delete local bookmark data according to user privacy needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/eric-tech-brief)
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/)
- [GitHub Trending](https://github.com/trending)
- [TechCrunch RSS feed](https://techcrunch.com/feed/)
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain-text news briefings with optional shell commands for public web requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article title, URL, source, date saved, and optional note or tag when bookmarking.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
