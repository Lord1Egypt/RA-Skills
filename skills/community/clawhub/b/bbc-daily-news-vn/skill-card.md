## Description:

Fetch the latest trending global news when users ask about current or breaking news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnquyen](https://clawhub.ai/user/mrnquyen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch BBC News Tieng Viet RSS headlines and summarize relevant current news items for user-facing responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate its news coverage as broad trending global news even though the implemented source is BBC Vietnamese RSS content.

Mitigation: Describe responses as BBC Vietnamese RSS-based summaries and avoid presenting them as comprehensive global trend coverage.

Risk: The skill runs local Python code and installs mutable, unpinned Python dependencies.

Mitigation: Review the source before installation, pin required packages, and run it in a controlled environment.

Risk: Fetched RSS entries are external reports and may be incomplete, stale, or inaccurate.

Mitigation: Treat RSS content as untrusted external news input and preserve source links so users can verify details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrnquyen/skills/bbc-daily-news-vn)
- [BBC Vietnamese RSS feed](https://feeds.bbci.co.uk/vietnamese/rss.xml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with source links from RSS-derived text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 10 BBC Vietnamese RSS entries and depends on network access plus Python package installation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
