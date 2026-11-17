## Description:

Steam Deck & Bazzite system management — gamescope, flatpak, podman, GPU, performance, game mode, system health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverod](https://clawhub.ai/user/silverod)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting Steam Deck or Bazzite users use this skill to propose system health checks, Gamescope troubleshooting, Flatpak and container management, performance diagnostics, and gaming setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network exposure commands can make a streaming service reachable outside the local device.

Mitigation: Require explicit user confirmation and review the intended service, port, and access controls before running network exposure commands.

Risk: Package changes, service restarts, and persistent configuration writes can alter the user's system state.

Mitigation: Present commands for review, explain the expected effect, and ask for confirmation before Flatpak install or update operations, service restarts, or persistent configuration writes.

Risk: Flatpak reset commands using `--delete-data` can remove application data.

Mitigation: Warn about data loss and recommend backups before suggesting destructive Flatpak reset commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are proposals for user review before execution.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
