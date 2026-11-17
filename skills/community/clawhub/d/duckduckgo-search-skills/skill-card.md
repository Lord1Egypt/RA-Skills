## Description:

Search the web using DuckDuckGo with no API key, supporting instant-answer and HTML search modes as a privacy-focused search alternative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cscsxx606](https://clawhub.ai/user/cscsxx606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run lightweight DuckDuckGo web searches, retrieve result titles, URLs, and snippets, and optionally return JSON or a short key-information summary without configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to DuckDuckGo.

Mitigation: Do not use the skill for secrets, private internal identifiers, sensitive prompts, or other confidential queries.

Risk: HTML search mode depends on DuckDuckGo public endpoints and may be rate limited or blocked.

Mitigation: Use modest request rates, retry later after 403 responses, and prefer a supported search API for production reliability requirements.

Risk: The --fetch-content option is documented as nonfunctional in this version.

Mitigation: Do not rely on webpage content fetching when planning workflows; use the returned result titles, URLs, snippets, JSON, and summaries only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cscsxx606/skills/duckduckgo-search-skills)
- [DuckDuckGo](https://duckduckgo.com)
- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/)
- [DuckDuckGo HTML search endpoint](https://html.duckduckgo.com/html/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text search result list or JSON object with results and optional summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count defaults to 5; HTML mode may be rate limited; --fetch-content is documented as nonfunctional in this version.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
