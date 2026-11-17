## Description:

Manage Freedcamp tasks, projects, groups, comments, notifications, and task lists via HMAC-SHA1 API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agrublev](https://clawhub.ai/user/agrublev)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent manage Freedcamp personal task workflows and project workflows, including task discovery, creation, updates, comments, task lists, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable Freedcamp session token and user ID in a local session cache.

Mitigation: Install only on trusted machines, protect the cache path, redirect it with FREEDCAMP_SESSION_PATH when needed, and remove the cache when rotating credentials or disabling the skill.

Risk: The skill requires Freedcamp API credentials that can access user or project data.

Mitigation: Use a dedicated low-privilege API credential where possible, avoid commands that print stored config values, and rotate credentials if exposure is suspected.

Risk: Several commands can create or modify Freedcamp content, including tasks, comments, and notification state.

Mitigation: Review agent-proposed write commands before execution and test write paths on low-impact or throwaway tasks first.

## Reference(s):

- [Freedcamp](https://freedcamp.com)
- [Freedcamp API v1](https://freedcamp.com/api/v1)
- [Reference and implementation notes](references/REFERENCE.md)
- [OpenClaw skills](https://docs.openclaw.ai/tools/skills)
- [OpenClaw skills config](https://docs.openclaw.ai/tools/skills-config)
- [OpenClaw config CLI](https://docs.openclaw.ai/cli/config)
- [AgentSkills format](https://agentskills.io/home)
- [ClawHub](https://docs.openclaw.ai/tools/clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI returns JSON on stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FREEDCAMP_API_KEY and FREEDCAMP_API_SECRET; the CLI stores a reusable session cache unless FREEDCAMP_SESSION_PATH redirects it.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
