## Description:

Manage Clawdbot agents: discover, profile, track capabilities, define routing hierarchy, and assign tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentandbot-design](https://clawhub.ai/user/agentandbot-design)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to maintain a central registry of Clawdbot agents, inspect agent capabilities, validate routing rules, and decide how tasks should move through approval and escalation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task escalation is configured around a hardcoded Telegram recipient, which can disclose task content outside the current session or workspace.

Mitigation: Remove the hardcoded recipient, disable external reporting by default, and require explicit confirmation before sending task content to any external channel.

Risk: Registry, routing, and health decisions rely on mock or placeholder logic, so assignment and status outputs may be inaccurate.

Mitigation: Replace mock discovery, authorization, registry parsing, and health checks with validated implementations before using the skill for operational task routing.

Risk: The security verdict is suspicious for workspaces containing private prompts, code, credentials, or business data.

Mitigation: Review and scan the skill before installation, and avoid using it in sensitive workspaces until the security guidance has been addressed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentandbot-design/skills/agents-manager)
- [Skill homepage](https://www.clawhub.com/skills/agents-manager)
- [Agent profile schema](references/agent-profile-schema.md)
- [Agent registry](references/agent-registry.md)
- [Task routing rules](references/task-routing-rules.md)
- [Health check template](references/health-check-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Mermaid, and shell command outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js for bundled helper scripts.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
