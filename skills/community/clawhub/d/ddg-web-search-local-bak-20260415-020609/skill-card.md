## Description:

Searches the web with DuckDuckGo's instant answer API and returns concise results for quick fact lookups or lightweight web search without browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[graafdefolkert-byte](https://clawhub.ai/user/graafdefolkert-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run DuckDuckGo lookups for quick facts, source URLs, and lightweight web search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an undocumented option that can open an external search-result URL in the user's local browser.

Mitigation: Review before installing, remove or document the browser-opening behavior, and require explicit user confirmation before opening external URLs.

## Reference(s):

- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/)
- [DuckDuckGo HTML search fallback](https://duckduckgo.com/html/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text search summaries with source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports when no strong instant-answer result is found and may provide fallback web result links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
