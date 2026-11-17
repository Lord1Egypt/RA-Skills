## Description:

Feishu Agent Mesh is a blueprint for wiring multiple OpenClaw agents into shared Feishu group chats through a relay, shared context, logging, routing, and human approval checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waytobetter619](https://clawhub.ai/user/waytobetter619)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to plan and configure Feishu-based coordination among multiple OpenClaw agents, including relay deployment, agent routing, shared logs, and approval checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill centralizes Feishu app secrets, verification tokens, encrypt keys, and bearer tokens.

Mitigation: Store credentials in a secret manager or protected environment variables, keep real secrets out of shared documents and JSON templates, and rotate any values exposed during setup.

Risk: Full-content message logging can capture sensitive chat content across Feishu groups.

Mitigation: Disable or minimize full-content logging unless approved by users and administrators, apply retention limits, and restrict log access to authorized operators.

Risk: An exposed callback or relay can become an entry point for unauthorized requests or replayed events.

Mitigation: Use HTTPS, verify Feishu tokens, add request signing and replay protection, whitelist approved chats, and grant only narrow per-agent permissions.

Risk: CLI fallback and broad relay-to-agent invocation can expand the blast radius of a misrouted or compromised task.

Mitigation: Remove CLI fallback for production deployments, enforce per-agent allowlists, and require human approval at configured checkpoints before sensitive actions continue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waytobetter619/skills/feishu-agent-mesh)
- [Architecture Guide](references/architecture.md)
- [Deployment Checklist](references/deployment-checklist.md)
- [Information Intake Form](references/info-collection-template.md)
- [Logging and Approval Schema](references/logging-schema.md)
- [Workflow Templates](references/workflow-templates.md)
- [Relay Configuration Example](scripts/relay-config.example.json)
- [Accounts Configuration Example](templates/accounts.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes relay, logging, approval, deployment, and workflow templates for Feishu agent coordination.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
