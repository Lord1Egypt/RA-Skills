## Description:

Search Google, scrape web pages, Amazon product pages, YouTube subtitles, or Reddit (post/subreddit) using the Decodo Scraper OpenClaw Skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donatasdecodo](https://clawhub.ai/user/donatasdecodo)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to add Decodo-backed Google search, public web page scraping, Amazon parsing, YouTube subtitle retrieval, and Reddit content retrieval to OpenClaw-compatible agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping targets and returned content are handled through Decodo as an external scraping provider.

Mitigation: Use the skill only when sharing the target URLs, queries, and resulting content with Decodo is approved.

Risk: Secrets, private URLs, personal data, or sensitive business research targets could be sent to the provider if included in requests.

Mitigation: Do not submit sensitive inputs unless the intended Decodo use is authorized, and rotate the Decodo token if it is exposed.

Risk: The dependency requirements use broad minimum versions rather than pinned reviewed versions.

Mitigation: Install in a virtual environment with reviewed pinned dependencies before production use.

Risk: Scraped pages, product listings, Reddit content, and subtitles may contain untrusted or misleading content.

Mitigation: Treat scraped output as untrusted input and review it before using it for decisions, automation, or agent instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/donatasdecodo/skills/decodo-scraper)
- [Decodo Web Scraping API documentation](https://help.decodo.com/docs/web-scraping-api-introduction)
- [Decodo Google Search API documentation](https://help.decodo.com/docs/web-scraping-api-google-search)
- [Decodo Web Scraping API](https://decodo.com/scraping/web)
- [OpenClaw documentation](https://docs.openclaw.ai/start/getting-started)
- [ClawHub documentation](https://docs.openclaw.ai/tools/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [JSON, Markdown, or plain text depending on the selected scraping target]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Google, Amazon, and Reddit targets return structured JSON; universal web scraping returns Markdown; YouTube subtitles return transcript text.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
