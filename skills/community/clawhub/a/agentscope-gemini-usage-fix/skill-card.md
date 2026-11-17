## Description:

Provides a workaround for AgentScope GeminiChatModel usage validation failures when cached_content_token_count is None.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using AgentScope with GeminiChatModel can diagnose cache_input_tokens validation errors and apply a temporary workaround.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workaround changes AgentScope behavior within the running Python process.

Mitigation: Apply it only for the documented validation error, and prefer the upstream fix once available in the installed AgentScope version.

## Reference(s):

- [AgentScope project](https://github.com/agentscope-ai/agentscope)
- [AgentScope issue #3077](https://github.com/agentscope-ai/agentscope/issues/3077)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a runtime workaround and a suggested upstream code change.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
