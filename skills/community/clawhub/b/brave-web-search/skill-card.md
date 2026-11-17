## Description:

Searches the web and returns ranked results or AI-generated summarized answers using the Brave Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kghamilton89](https://clawhub.ai/user/kghamilton89)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to perform real-time web lookups, retrieve ranked search results, and request concise answer summaries through Brave APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Brave using configured Brave API keys.

Mitigation: Avoid sensitive personal, credential, legal, medical, or confidential business queries unless that external sharing is acceptable.

Risk: Improper command invocation could expose user-supplied queries to shell parsing.

Mitigation: Pass command names and query values as discrete arguments, such as an execFile-style argv array.

## Reference(s):

- [Brave Web Search ClawHub skill page](https://clawhub.ai/kghamilton89/skills/brave-web-search)
- [Brave Search API endpoint](https://api.search.brave.com/res/v1)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON results or Markdown-facing summaries derived from JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_SEARCH_API_KEY for search and BRAVE_ANSWERS_API_KEY for summarized answers.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
