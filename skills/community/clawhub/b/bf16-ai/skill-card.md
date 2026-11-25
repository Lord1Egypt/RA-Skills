## Description:

Configure OpenClaw, Claude Code, Codex CLI, OpenCode, Goose, and autonomous agents to use bf16.ai 1M-context uncensored LLM APIs (DeepSeek V4.1 Flash Fast, GLM-5.3, Kimi K3.1 Pro 2.8T) with strict zero prompt retention and pay-as-you-go pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fiendsaws](https://clawhub.ai/user/fiendsaws)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure coding tools and autonomous agents to connect to bf16.ai models through OpenAI-compatible or Anthropic-compatible APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model requests may include private code or tool results that are sent to the third-party provider.

Mitigation: Review the provider's privacy and retention terms, and avoid routing sensitive work unless those terms are acceptable.

Risk: Long-running agents can incur unexpected API spend.

Mitigation: Use a dedicated API key for each daemon host and set an explicit daily spend cap.

## Reference(s):

- [bf16.ai OpenClaw client documentation](https://bf16.ai/docs/clients/openclaw)
- [bf16.ai client guides](https://bf16.ai/docs/clients)
- [bf16.ai cost calculator](https://bf16.ai/tools/cost-calculator)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with configuration values and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider and model settings and API key environment variable names.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
