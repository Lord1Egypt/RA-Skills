## Description:

Search Google, scrape web pages, Amazon product pages, YouTube subtitles, or Reddit post and subreddit content using the Decodo Scraper OpenClaw Skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donatasdecodo](https://clawhub.ai/user/donatasdecodo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to give OpenClaw-compatible agents access to Decodo-backed web scraping for search results, public webpages, Amazon pages, YouTube subtitles, and Reddit content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, search terms, video IDs, Reddit or Amazon targets, request metadata, and the Decodo API token are sent to Decodo.

Mitigation: Avoid private/internal URLs and sensitive investigations unless the Decodo account, policies, and intended use allow that data sharing.

Risk: Runtime dependencies are declared with minimum versions rather than pinned versions.

Mitigation: Pin and review dependency versions in controlled deployments.

## Reference(s):

- [Decodo Web Scraping API Documentation](https://help.decodo.com/docs/web-scraping-api-introduction)
- [Decodo Google Search API Documentation](https://help.decodo.com/docs/web-scraping-api-google-search)
- [Decodo Web Scraping API](https://decodo.com/scraping/web)
- [OpenClaw Getting Started](https://docs.openclaw.ai/start/getting-started)
- [ClawHub Skill Page](https://clawhub.ai/donatasdecodo/skills/decodo-scraper-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON, Markdown, or plain text transcript depending on the selected scraping target.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DECODO_AUTH_TOKEN and sends selected targets to Decodo's Web Scraping API.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
