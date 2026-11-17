## Description:

Build apps with the Claude API or Anthropic SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to choose the right Claude API, Anthropic SDK, or Agent SDK surface and generate language-specific integration guidance, code examples, shell commands, and configuration advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples for production integration code may be incomplete, outdated, or unsuitable for a specific application.

Mitigation: Review generated code and configuration before production use, verify against current official documentation, and test behavior with the target SDK and model.

Risk: Agent SDK examples include high-impact permission modes that can allow file edits, command execution, or reduced approval prompts.

Mitigation: Prefer default or plan permission modes, require approval for destructive operations, and limit tool access to the minimum required for the task.

Risk: MCP examples may execute mutable packages such as npx @latest.

Mitigation: Pin MCP package versions and review MCP server behavior before enabling it in an agent environment.

Risk: Prompts, files, tool results, conversation history, API keys, or database credentials may be sent to external APIs or used by generated examples.

Mitigation: Redact sensitive data before sending requests, keep API keys in environment variables or secret stores, and use least-privilege credentials for databases and tools.

## Reference(s):

- [Claude API live documentation sources](artifact/shared/live-sources.md)
- [Claude API tool use concepts](artifact/shared/tool-use-concepts.md)
- [Claude API error codes](artifact/shared/error-codes.md)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Anthropic TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python)
- [Claude Agent SDK TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with language-specific code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests, SDK usage patterns, model selection guidance, streaming examples, tool-use guidance, and security cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
