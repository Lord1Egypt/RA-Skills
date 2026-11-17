## Description:

CLI tool to clean up stopped Docker containers, unused images, volumes, and networks to free up disk space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT

## Use Case:

Developers and DevOps engineers use this skill to inspect Docker resource usage and remove stopped containers, unused images, volumes, and networks to reclaim disk space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup commands can delete Docker containers, images, volumes, or networks, and security evidence notes that confirmations may not match the documentation.

Mitigation: Review the exact cleanup scope before execution, start with dry-run mode, and avoid force or yes flags until behavior has been verified in the target environment.

Risk: Volume cleanup can remove persistent data.

Mitigation: Back up important volumes and confirm that no needed services depend on them before running volume cleanup.

Risk: Running against production or remote Docker contexts can remove resources from the wrong environment.

Mitigation: Verify the active Docker context and prefer staging or maintenance windows for non-local cleanup.

Risk: Dry-run volume and network counts may not be an exact deletion plan.

Mitigation: Inspect resources with Docker commands before deletion and use granular cleanup flags when exact control is needed.

## Reference(s):

- [Docker Container Cleaner on ClawHub](https://clawhub.ai/derick001/skills/docker-container-cleaner)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [CLI text or JSON with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and Docker CLI access; Docker SDK for Python is optional.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
