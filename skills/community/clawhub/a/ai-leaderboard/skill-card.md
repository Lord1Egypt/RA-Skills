## Description:

Queries public AI model and application leaderboards for model rankings, OpenRouter model IDs, pricing, benchmarks, and provider comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luduoxin](https://clawhub.ai/user/luduoxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and AI product teams use this skill to compare public model leaderboards, find OpenRouter model identifiers, and review pricing or benchmark signals before selecting models or providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run shell commands and browser automation against external ranking sites through an unpinned global browser CLI.

Mitigation: Use a pinned local agent-browser installation in a restricted environment and review commands before execution.

Risk: The OpenRouter chat-completions example may send an API key and message content to OpenRouter if executed.

Mitigation: Do not run the chat-completions example unless that data sharing is intended; prefer the public model catalog queries for lookup tasks.

Risk: Leaderboard, pricing, and benchmark results are live external data and can change over time.

Mitigation: Include the queried source and query time in user-facing results and avoid treating leaderboard snapshots as permanent facts.

## Reference(s):

- [Artificial Analysis](https://artificialanalysis.ai/)
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/leaderboards/models)
- [Artificial Analysis LLM API Providers](https://artificialanalysis.ai/leaderboards/providers)
- [OpenRouter Rankings](https://openrouter.ai/rankings)
- [OpenRouter Apps](https://openrouter.ai/apps)
- [OpenRouter Models](https://openrouter.ai/models)
- [Pinchbench](https://pinchbench.com/)
- [ClawHub Skill Page](https://clawhub.ai/luduoxin/skills/ai-leaderboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and terminal-formatted text with tables, model identifiers, pricing details, and example API commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live public ranking sites and OpenRouter catalog data.]

## Skill Version(s):

1.20.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
