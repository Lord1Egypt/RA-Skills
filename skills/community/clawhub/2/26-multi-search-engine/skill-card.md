## Description:

Multi search engine integration with 17 engines (8 CN + 9 Global), advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries with no API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to construct web search queries across Chinese and global search engines, including advanced operators, time filters, privacy-oriented providers, DuckDuckGo Bangs, and WolframAlpha knowledge queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to third-party search providers and can expose sensitive terms, personal data, credentials, confidential investigation topics, or internal identifiers.

Mitigation: Use only non-sensitive queries unless the user is comfortable sharing them with the selected search provider, and choose the CN or global engine based on locale and privacy needs.

## Reference(s):

- [International Search Guide](artifact/references/international-search.md)
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/skills/26-multi-search-engine)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline JavaScript web_fetch examples and search URL templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces search-engine URL patterns and query construction guidance; no API keys are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
