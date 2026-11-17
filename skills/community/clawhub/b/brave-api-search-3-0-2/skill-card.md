## Description:

Real-time web search, autosuggest, and AI-powered answers using the official Brave Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujm2012](https://clawhub.ai/user/liujm2012)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Brave Search web results, query suggestions, and AI-grounded answers with citations when current external web information is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted search text may execute local commands in shell-based runtimes that interpolate tool command templates.

Mitigation: Use only runtimes that pass tool arguments without shell interpretation, or change the command templates to argument-array execution before deployment.

Risk: Search queries and answer prompts are sent to the third-party Brave API.

Mitigation: Avoid submitting secrets or sensitive personal or company data, and scope Brave API keys to this service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liujm2012/skills/brave-api-search-3-0-2)
- [Brave Search API Dashboard](https://api-dashboard.search.brave.com)
- [Brave Search API Documentation](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls]

**Output Format:** [Markdown-formatted search results, suggestions, and cited answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_SEARCH_API_KEY and BRAVE_ANSWERS_API_KEY; answers may include citations and token usage.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also lists 3.0.2, 3.0.0, and 2.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
