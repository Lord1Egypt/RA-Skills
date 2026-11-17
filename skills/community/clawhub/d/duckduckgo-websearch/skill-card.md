## Description:

Perform private, high-quality web searches using DuckDuckGo's Instant Answer API with fallback to top links and snippets without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianwchoi](https://clawhub.ai/user/ianwchoi)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run quick DuckDuckGo web searches, return concise summaries and top links, and avoid paid search API keys when privacy-friendly search is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to DuckDuckGo.

Mitigation: Avoid queries containing secrets, credentials, private customer data, or internal prompts.

Risk: Dependency ranges may permit compatible updates during install.

Mitigation: Use locked installs such as npm ci and review lockfile changes before deployment.

Risk: Search results and snippets can be stale, incomplete, or misleading.

Mitigation: Review source links before acting on returned information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ianwchoi/skills/duckduckgo-websearch)
- [Usage examples](references/usage_examples.md)
- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/)
- [DuckDuckGo HTML search endpoint](https://duckduckgo.com/html/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON search result object with query, summary, links, source, and notes fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 5 links with titles and snippets; summaries may be empty when DuckDuckGo has no instant answer.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
