## Description:

Robust Docker volume migration and backup using per-volume encrypted archives and registry-based transport. Supports dry-runs, container exclusion, and safe restoration without executing untrusted code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to back up or migrate Docker-managed volumes through a Docker registry using encrypted per-volume archives. It is intended for hosts where the user can safely grant Docker-level access and control container stop, push, pull, and restore operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can affect all Docker volumes and running containers on the host.

Mitigation: Run --dry-run first, review the planned containers and volumes, and use --exclude-stop for critical containers that must remain available.

Risk: Encrypted backups are uploaded to a registry and should still be treated as sensitive material.

Mitigation: Use a private registry repository, verify the destination image name before pushing, and restrict repository access.

Risk: The backup password may be exposed through shell history, CI logs, or process/container metadata.

Mitigation: Avoid entering production passwords in logged shells or CI output, and run the workflow only in controlled environments.

Risk: Restore can replace data in same-named Docker volumes.

Mitigation: Confirm the source image and target volume names before restore, prefer digest-pinned restore images, and keep an independent backup of important destination data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugvfpdcuwfnh/skills/docker-volume-backup-or-restore)
- [Limitations and Tradeoffs](references/limitations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup and restore instructions for Docker volumes; execution may create local list files and encrypted registry images when the provided shell workflow is run.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
