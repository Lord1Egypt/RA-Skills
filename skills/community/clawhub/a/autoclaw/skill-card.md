## Description:

Autoclaw automates health monitoring, scheduled backups, and process logging for AI assistant workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shayuqiang671-rgb](https://clawhub.ai/user/shayuqiang671-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Autoclaw to monitor AI assistant workspaces, back up key configuration and memory files, and log health and process checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext backups may contain private workspace memory, configuration, and database contents.

Mitigation: Run the skill only on an intended workspace, restrict access to the backup directory, and remove or protect backups after use.

Risk: A hard-coded Administrator workspace path may target the wrong local workspace.

Mitigation: Verify or change the workspace path before execution and avoid running with unnecessary privileges.

Risk: Process monitoring settings may not match the user's environment.

Mitigation: Review monitored process names, script paths, and restart behavior before enabling monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shayuqiang671-rgb/skills/autoclaw)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead an agent to run workspace health checks, create plaintext backups, and write timestamped logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
