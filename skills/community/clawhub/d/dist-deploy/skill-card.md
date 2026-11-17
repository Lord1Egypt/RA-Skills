## Description:

Deploy static build output to an SSH-reachable server using a parameterized upload and directory swap, with backups, ownership fixup, and an optional post-deploy hook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leafotto](https://clawhub.ai/user/leafotto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to package and deploy static build output to a server they can reach over SSH, with configurable target paths, backups, ownership, and service reload hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command quoting may run unintended commands during deployment.

Mitigation: Fix and review Bash parameter quoting, verify the destination and post-deploy hook, and use a restricted deployment account.

Risk: Incomplete failure recovery could leave the site offline after the live directory changes.

Mitigation: Improve and verify recovery steps before production use, and keep independent backups. Live-server recovery has not been tested.

Risk: Fresh mode deletes the previous release, while backup retention removes older backups.

Mitigation: Confirm the target path and backup policy before running; use fresh mode only when the previous release is disposable.

## Reference(s):

- [dist-deploy on ClawHub](https://clawhub.ai/leafotto/skills/dist-deploy)
- [Publisher profile: leafotto](https://clawhub.ai/user/leafotto)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with PowerShell and Bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use caller-supplied source, SSH server, target path, and optional deployment settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
