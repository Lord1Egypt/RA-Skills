## Description:

Find question-based Google Autocomplete suggestions for any topic by prepending question modifiers such as what, how, and why to a seed topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Content strategists, SEO researchers, and agent builders use this skill to discover real question-style search suggestions for a topic and generate prompt or content angles. It can also enrich suggestions with monthly search volume when DataForSEO credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword queries are sent to Google Autocomplete during normal use, and optionally to DataForSEO when search volume is requested.

Mitigation: Avoid sensitive client, legal, medical, or confidential research terms unless sharing them with those third-party services is acceptable.

Risk: The optional DataForSEO volume lookup can read credentials from environment variables or macOS Keychain.

Mitigation: Use --volume only in environments where those credentials are intentionally configured and authorized for the research task.

Risk: Running many keyword queries quickly can trigger temporary IP blocks from the unofficial Google Autocomplete endpoint.

Mitigation: Use the documented --delay option, especially for batch or parallel research runs.

## Reference(s):

- [Google Autocomplete suggest endpoint](https://suggestqueries.google.com/complete/search)
- [DataForSEO Google Ads search volume API endpoint](https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown-style text with headings and bullets, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional search-volume enrichment adds monthly volume values when DataForSEO credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
