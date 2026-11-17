## Description:

Builds, manages, and troubleshoots WhatsApp bots using the BuilderBot Cloud (BBC) MCP Tool v2.0, including project and flow management, answer configuration, validation, deployment, recovery, and common business bot patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leifermendez](https://clawhub.ai/user/leifermendez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business automation builders use this skill to create, update, validate, deploy, and troubleshoot WhatsApp bots on BuilderBot Cloud for appointments, support escalation, lead capture, order status, media handling, and AI-assisted conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create, update, validate, deploy, reboot, and delete BuilderBot Cloud bot resources.

Mitigation: Require explicit confirmation before destructive actions, verify resource state after each mutation, and run validation before deployment.

Risk: CRM, dashboard, webhook, website-scraping, and media URL configuration can expose customer data or connect the bot to external systems.

Mitigation: Review all external URLs and integrations before use, and define privacy notices, consent, retention, and access-control rules for collected or forwarded conversation data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leifermendez/skills/bbc-skill-tool)
- [Advanced Patterns](artifact/advanced-patterns.md)
- [Vertical Templates](artifact/verticals.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with structured examples, tool-call sequences, configuration snippets, and bot reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute BuilderBot Cloud mutations, deployment actions, webhook configuration, website scraping setup, media URL configuration, and recovery steps through the connected MCP tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
