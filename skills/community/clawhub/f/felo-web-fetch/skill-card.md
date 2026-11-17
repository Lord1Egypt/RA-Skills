## Description:

Fetch web page content from a URL using Felo Web Extract API for scraping, article extraction, URL-to-markdown or URL-to-text conversion, and optional readability processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to fetch webpage content from a supplied URL and return it as markdown, text, HTML, or a JSON API response for downstream summarization or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, selectors, and fetched page content are sent to Felo.

Mitigation: Use only for content approved for sharing with Felo; avoid private intranet pages, authenticated links, signed URLs, secrets, regulated data, and confidential content unless sharing is approved.

Risk: FELO_API_BASE can redirect requests and expose the API key to an alternate endpoint.

Mitigation: Keep FELO_API_BASE unset unless the endpoint is controlled and trusted, and rotate FELO_API_KEY if exposure is suspected.

Risk: An unpinned global CLI install path can introduce unreviewed code changes.

Mitigation: Prefer the bundled script or a pinned, reviewed CLI version over an unpinned global npm install.

## Reference(s):

- [Felo Web Extract API](https://openapi.felo.ai/docs/api-reference/v2/web-extract.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/felo-web-fetch)
- [Publisher profile](https://clawhub.ai/user/wangzhiming1999)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Fetched page content as markdown, plain text, HTML, or full JSON response depending on options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FELO_API_KEY and a user-supplied URL; supports output format, CSS selector targeting, readability mode, crawl mode, timeout, and JSON response options.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
