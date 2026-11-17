## Description:

Collects topic-based news and produces Korean three-line article summaries plus a Markdown briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinu4you](https://clawhub.ai/user/jinu4you)

### License/Terms of Use:

ISC

## Use Case:

External users and developers use this agent to gather recent news for a topic, summarize returned articles in Korean, rank them by importance, and generate a concise Markdown briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search topics, returned article excerpts, and generated summaries are shared with Tavily and the configured LLM provider.

Mitigation: Use limited-scope API keys, avoid sensitive topics, and disclose third-party data sharing to users.

Risk: News content and generated summaries may be incomplete, misleading, or affected by prompt-injection-prone source material.

Mitigation: Treat summaries, rankings, and links as untrusted until independently checked, and validate that model output preserves source URLs and expected score ranges.

Risk: The artifact includes a startup mock job that can run a sample Bitcoin digest automatically.

Mitigation: Remove or gate the mock job before production deployment.

Risk: External API credentials are required for normal operation.

Mitigation: Store keys in environment variables, rotate them regularly, and update dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinu4you/skills/agent-news-digest)
- [Tavily search API endpoint](https://api.tavily.com/search)
- [Groq OpenAI-compatible API endpoint](https://api.groq.com/openai/v1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Structured JSON job result containing article records and a Korean Markdown briefing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the topic, period, total article count, article summaries, source URLs, published dates when available, importance scores, and a brief.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
