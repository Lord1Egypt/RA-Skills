## Description:

Fetches RSS feeds from 90 top Hacker News blogs curated by Karpathy, uses AI to score and filter articles, and generates a daily digest in Markdown with Chinese-translated titles, category grouping, trend highlights, and visual statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royxiao08](https://clawhub.ai/user/royxiao08)

### License/Terms of Use:


## Use Case:

Developers, engineers, and technical readers use this skill to collect recent articles from curated technology RSS feeds, rank them with an AI model, and produce a readable daily Markdown digest. It is intended for users who want a concise AI, software engineering, security, tools, and technology commentary briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store an API key in a predictable plaintext home-directory configuration file.

Mitigation: Use environment variables for API keys when possible and remove ~/.hn-daily-digest/config.json if it contains a real key.

Risk: The execution flow can run an unpinned Bun runtime package.

Mitigation: Prefer a preinstalled or pinned Bun runtime before running the digest script.

Risk: Custom OpenAI-compatible endpoints can expose prompts and article data to an untrusted service.

Mitigation: Use custom OpenAI-compatible endpoints only when you control and trust the endpoint.

## Reference(s):

- [AI Daily Digest on ClawHub](https://clawhub.ai/royxiao08/skills/ai-daily-digest)
- [Hacker News Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/)
- [Andrej Karpathy RSS source reference](https://x.com/karpathy)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest file with article rankings, summaries, category sections, Mermaid charts, ASCII charts, and a short terminal preview.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The digest is written to a user-selected Markdown path, defaulting to a dated digest file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
