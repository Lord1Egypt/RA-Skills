## Description:

Scrape Substack newsletters and articles when users need to search Substack, find newsletter posts, extract Substack content, or monitor Substack publications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to scrape Substack publication URLs through an Apify Actor, then summarize article metadata and optionally full article content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example commands place the Apify token in URLs where it may be logged or exposed.

Mitigation: Use a narrowly scoped Apify token, avoid shell tracing or command logging, and prefer header-based authorization where supported.

Risk: Scraping unsuitable Substack URLs can collect content that is not approved for the intended use.

Mitigation: Use only public or approved Substack URLs and review extracted results before sharing or exporting them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marcindudekdev/skills/apify-substack-scraper)
- [Apify Actor API Endpoint](https://api.apify.com/v2/acts/BULaGFURBV7WG3K81)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON result handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN plus curl and jq; supported inputs include urls, maxArticles, and includeContent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
