## Description:

Token-based context compaction for local models (MLX, llama.cpp, Ollama) that don't report context limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emberdesire](https://clawhub.ai/user/emberdesire)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to keep long-running local-model conversations within context limits by estimating token use, summarizing older turns, and preserving recent messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prior conversation content may be summarized through the active LLM despite local-only privacy claims.

Mitigation: Pin and inspect the package before installation, and configure or require a strict local-only summarization model when privacy matters.

Risk: Lossy summaries can influence later agent context and omit details needed for high-assurance workflows.

Mitigation: Avoid enabling the skill for high-assurance workflows unless users review compacted context and accept summary loss.

Risk: The gateway stats path is under-scoped for multi-user or remotely reachable gateways.

Mitigation: Do not use the stats gateway method in shared or remotely reachable deployments until the session path handling is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emberdesire/skills/context-compactor)
- [OpenClaw Compaction Documentation](https://docs.openclaw.ai/concepts/compaction)
- [npm Package](https://www.npmjs.com/package/jasper-context-compactor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are capped by summaryMaxTokens, and context size is estimated from character length.]

## Skill Version(s):

0.3.8 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
