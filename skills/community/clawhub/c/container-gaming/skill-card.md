## Description:

Container-based gaming setup on Linux covering Podman, Distrobox, Flatpak gaming, Wine/Proton containers, Sunshine streaming, and related troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverod](https://clawhub.ai/user/silverod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and Linux gamers use this skill to set up and troubleshoot containerized gaming workflows, Flatpak game apps, Wine/Proton tooling, and Sunshine/Moonlight streaming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands run as administrator can execute unreviewed or changing internet-hosted code.

Mitigation: Prefer distro packages or pinned, verified installers, and review commands before execution.

Risk: Unpinned container images can change unexpectedly and may broaden access when host paths or display sockets are shared.

Mitigation: Use pinned and verified images, mount only a dedicated game directory, and avoid X11 sharing where possible.

Risk: Game-streaming services can expose local services or desktops if opened before authentication and access controls are configured.

Mitigation: Configure Sunshine authentication first, limit remote access to trusted devices, and expose services over Tailscale only after those controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silverod/skills/container-gaming)
- [ClawHub publisher profile](https://clawhub.ai/user/silverod)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux-focused guidance; many workflows require Podman, Flatpak, or Distrobox.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
