## Description:

Search the web using AI models with built-in search capability. Use for live information, news, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cznorth](https://clawhub.ai/user/cznorth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run live web searches through DeepSeek search-enabled chat and reasoning models from an agent or command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the bearer credential are sent to the configured third-party API endpoint.

Mitigation: Use a limited API key, avoid sending secrets or private code in queries, and configure AI_SEARCH_BASE_URL only to a provider you trust.

Risk: The release includes a shared public API key and has limited privacy and scoping disclosure.

Mitigation: Prefer your own scoped credential and review the skill before installing or running it.

## Reference(s):

- [DeepSeek AI Search on ClawHub](https://clawhub.ai/cznorth/skills/deepseek-ai-search)
- [cznorth Publisher Profile](https://clawhub.ai/user/cznorth)
- [Default AI Search API endpoint](https://ai.ch66.top)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown-formatted search results, optionally including reasoning and usage statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests library, and AI_SEARCH_API_KEY; AI_SEARCH_BASE_URL can redirect requests to a configured provider.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
