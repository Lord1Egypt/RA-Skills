## Description:

Easy English Tool gives agents access to an English-learning MCP and REST service for vocabulary, articles, quizzes, copy practice, text-to-speech, pronunciation evaluation, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengkane](https://clawhub.ai/user/dengkane)

### License/Terms of Use:

MIT-0

## Use Case:

External English learners and their agents use this skill to manage daily study workflows, including vocabulary review, level selection, article practice, quizzes, writing practice, TTS playback, and progress checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends login and learning data to the remote english.geeyo.com service.

Mitigation: Install only when the user trusts that service with account and study data.

Risk: The REST fallback documents user-ID-based access, which can expose or misuse learning records if IDs are shared.

Mitigation: Prefer the MCP login flow and treat raw user IDs as sensitive.

Risk: Some actions can submit scores, change levels, create content, or delete articles.

Mitigation: Confirm with the user before performing state-changing study actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dengkane/skills/easy-english-tool)
- [Production English-learning service](https://english.geeyo.com)
- [Streamable HTTP MCP endpoint](https://english.geeyo.com/api/mcp/http)
- [SSE MCP endpoint](https://english.geeyo.com/api/mcp/sse)
- [Service health check](https://english.geeyo.com/api/health)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, shell commands, markdown]

**Output Format:** [Markdown guidance with JSON configuration snippets and MCP or REST call details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke remote MCP or REST operations against english.geeyo.com when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
