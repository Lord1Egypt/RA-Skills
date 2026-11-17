## Description:

Crawl/scrape and extract content from any webpage URL. Returns the page content as clean text or raw HTML. Use this when you need to read the full contents of a specific web page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okradze](https://clawhub.ai/user/okradze)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to crawl a specific webpage URL and return either clean text for reading or raw HTML for page-structure inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Desearch API key is used for requests to Desearch, and Desearch may receive the target URL and crawl results.

Mitigation: Use the skill only with URLs appropriate for the configured Desearch account and avoid sensitive internal URLs unless the service is trusted for that data.

Risk: Crawling can create cost or policy exposure if used against URLs the user is not allowed to crawl.

Mitigation: Confirm crawl permissions before use and consider Desearch account cost limits.

## Reference(s):

- [Desearch Homepage](https://desearch.ai)
- [Desearch Web Crawl API Reference](https://desearch.ai/docs/api-reference/get-web-crawl)
- [Desearch Console](https://console.desearch.ai)
- [ClawHub Skill Page](https://clawhub.ai/okradze/skills/desearch-crawl)

## Skill Output:

**Output Type(s):** [Text, HTML, Shell commands, Guidance]

**Output Format:** [Plain text or raw HTML printed to stdout; JSON may be printed for API error responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and sends crawl requests to Desearch.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
