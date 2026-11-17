## Description:

Monitors API billing failures, alerts the owner and admin when action is needed, and guides fallback model switching and incident logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to detect billing-related API failures, notify the responsible owner or admin, and switch to a configured fallback model when service continuity requires it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can source executable local context before using owner, admin, log, and fallback settings.

Mitigation: Use only trusted local configuration and prefer a non-executable config format for deployment values.

Risk: Scheduled health checks can use credential-backed provider API calls and write incident logs.

Mitigation: Limit checks to explicitly approved provider keys, use dedicated monitoring credentials where possible, and set appropriate log retention and file permissions.

Risk: The skill can change model configuration automatically during a billing incident.

Mitigation: Require clear owner or admin control before automatic model switching and document the configured fallback model.

## Reference(s):

- [Billing Monitor on ClawHub](https://clawhub.ai/netanel-abergel/skills/billing-monitor)
- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages)
- [OpenAI Chat Completions API endpoint](https://api.openai.com/v1/chat/completions)
- [Google Generative Language models endpoint](https://generativelanguage.googleapis.com/v1beta/models)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes alert message templates, provider health-check commands, fallback configuration guidance, and incident logging steps.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
