## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wetor](https://clawhub.ai/user/wetor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to run Tavily web searches, news searches, and URL extraction when they need concise source-backed web context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, requested URLs, and the user's Tavily API key are sent to Tavily's API.

Mitigation: Use only for information that Tavily is approved to process, and avoid confidential prompts, private internal URLs, or sensitive data unless Tavily is an approved provider.

Risk: Web search and extracted page content can be incomplete, outdated, or misleading.

Mitigation: Review returned sources and extracted content before relying on the output for decisions.

## Reference(s):

- [Tavily homepage](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/wetor/skills/baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with answers, source lists, relevance scores, and extracted page content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and TAVILY_API_KEY. Sends search queries and requested URLs to Tavily's API.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
