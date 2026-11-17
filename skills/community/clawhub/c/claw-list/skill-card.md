## Description:

Claw List helps agents manage todo lists through a self-hosted REST API with per-agent lists, categories, priorities, due dates, and a web UI for oversight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let OpenClaw agents create, read, update, and complete task lists through a central service instead of direct database access. It is suited for self-hosted multi-agent task tracking where human operators also need a browser view of agents, lists, and items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled server has serious access-control and UI-safety concerns according to the authoritative security evidence.

Mitigation: Deploy only on a trusted local or tightly controlled internal network until authentication, HTTPS guidance, and UI escaping are reviewed and fixed.

Risk: Task notes can contain sensitive conversation context that may be readable or editable by anyone who can reach the API or UI.

Mitigation: Do not store secrets, credentials, private conversation excerpts, or sensitive personal data in task titles or notes.

Risk: Agents with broad read scope can view lists and items owned by other agents.

Mitigation: Keep agent scope at the default own setting unless cross-agent visibility is explicitly required and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mbojer/skills/claw-list)
- [Overview](docs/overview.md)
- [API Reference](docs/api.md)
- [Server Setup](server/README.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with REST request details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update task data through the configured Claw List API.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
