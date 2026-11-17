## Description:

Free web search using Claude Code CLI or Codex CLI's built-in WebSearch tool, with no Tavily, Brave, or Exa API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinghan23](https://clawhub.ai/user/jinghan23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to perform web searches through an authenticated Claude Code CLI or Codex CLI when other search providers are unavailable, unconfigured, or out of quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent through authenticated Claude Code or Codex CLI sessions.

Mitigation: Avoid secrets, credentials, private customer data, and proprietary internal questions in search queries.

Risk: The Codex fallback may run a broader nested agent than users expect for simple search.

Mitigation: Prefer the Claude backend or a clearly sandboxed Codex configuration, and review broad automatic activation for generic search requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinghan23/skills/claudecode-websearch)
- [Claude Code](https://claude.ai/code)
- [OpenAI Codex CLI](https://github.com/openai/codex)
- [OpenAI Codex](https://openai.com/codex)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary with source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search query, optional maximum result count, and optional backend selection influence the returned summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
