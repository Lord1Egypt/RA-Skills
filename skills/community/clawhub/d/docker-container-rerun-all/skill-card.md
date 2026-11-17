## Description:

Checks remembered Docker-run containers sequentially for newer images and, when explicitly requested, recreates those needing updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check Docker-run containers with saved recreate commands and, after review, refresh containers whose images changed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying updates can stop, remove, and recreate running containers.

Mitigation: Run the default check first; use --apply only after explicitly approving the affected containers and their saved recreate commands.

Risk: Saved Docker commands may grant elevated access through docker.sock, privileged mounts, or host paths; mutable image tags can change unexpectedly.

Mitigation: Inspect each saved command, its mounts and privileges, and the images to be pulled before applying updates.

## Reference(s):

- [Docker Container Rerun All on ClawHub](https://clawhub.ai/ugvfpdcuwfnh/skills/docker-container-rerun-all)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Chinese-language grouped report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups updated, up-to-date, and failed containers; includes image and status details when available.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
