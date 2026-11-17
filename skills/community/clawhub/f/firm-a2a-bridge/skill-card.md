## Description:

Agent-to-Agent (A2A) Protocol RC v1.0 bridge for OpenClaw agents that enables agent discovery, identity cards, task lifecycle management, push notification configuration, task cancellation, and SSE subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to expose OpenClaw agents through the A2A Protocol RC v1.0, including agent card generation and validation, task lifecycle operations, discovery, push notification configuration, cancellation, and SSE subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact remote agent URLs, configure task webhooks, and subscribe to task events.

Mitigation: Review target URLs and webhook destinations before use, approve only trusted endpoints, and keep remote task subscriptions scoped to the intended agent workflow.

Risk: The skill may read local SOUL.md files provided to it while generating or discovering Agent Cards.

Mitigation: Provide only intended SOUL.md paths and review generated Agent Card JSON before publishing or sharing it.

Risk: Most operating documentation is in French, which can reduce review quality for non-French users.

Mitigation: Translate and human-review the documentation and operating details before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-a2a-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and MCP tool-call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or validate Agent Card JSON, task and webhook configuration details, and status or event subscription guidance.]

## Skill Version(s):

2.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
