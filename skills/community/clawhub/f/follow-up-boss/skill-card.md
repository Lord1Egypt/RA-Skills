## Description:

CLI for interacting with the Follow Up Boss API. Manage people, notes, tasks, events, deals, webhooks, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Follow Up Boss CRM records and activity from a Node.js CLI. It supports reading and modifying people, notes, tasks, events, deals, communications logs, webhooks, sources, users, and global search results through the Follow Up Boss API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify Follow Up Boss CRM data.

Mitigation: Install it only where the agent is authorized to access CRM data and use the least-privileged API key available.

Risk: Delete and update operations, including webhook deletion, can change production CRM behavior.

Mitigation: Require explicit human approval before running destructive or mutating commands.

Risk: The skill depends on a Follow Up Boss API key stored in the environment.

Mitigation: Avoid broad credential exposure and keep production credentials out of shared agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielfoch/skills/follow-up-boss)
- [Follow Up Boss API v1 endpoint](https://api.followupboss.com/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON]

**Output Format:** [Markdown usage guidance, shell commands, and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FUB_API_KEY; optional FUB_SYSTEM_KEY and FUB_SYSTEM_NAME headers are supported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
