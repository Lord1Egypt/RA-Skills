## Description:

Fetches AI and technology news or custom-topic updates from RSS feeds, Tavily, Twitter/X, and YouTube, summarizes them with OpenAI, DeepSeek, or Claude, and posts an English editorial digest to Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottll](https://clawhub.ai/user/scottll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent news and trending content for a topic, generate an editorial digest, and publish it to a configured Discord channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested topics and gathered article, tweet, and video metadata may be sent to third-party search, social, video, and AI providers.

Mitigation: Provide only the API keys needed for the chosen mode and avoid running the skill on sensitive topics.

Risk: AI-generated summaries from untrusted web and social content can be inaccurate or misleading before being posted to Discord.

Mitigation: Use dry-run first and review the generated digest before enabling Discord posting.

Risk: Discord posts may include generated links or mentions derived from gathered content.

Mitigation: Review Discord mention and link handling before deployment and post only to an appropriate channel.

Risk: Runtime dependencies are installed by uv from inline script metadata rather than pinned hashes.

Mitigation: Prefer a version with pinned dependencies before using the skill in a higher-trust workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottll/skills/ai-news-aggregator-sl)
- [Publisher profile](https://clawhub.ai/user/scottll)
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
- [OpenAI API keys](https://platform.openai.com/api-keys)
- [DeepSeek API keys](https://platform.deepseek.com/api_keys)
- [Anthropic Console](https://console.anthropic.com)
- [Tavily](https://app.tavily.com)
- [Google Cloud Console](https://console.cloud.google.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown digest, terminal status text, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print a dry-run preview or post chunked Markdown messages to Discord.]

## Skill Version(s):

1.2.8 (source: server release metadata; artifact frontmatter says 1.5.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
