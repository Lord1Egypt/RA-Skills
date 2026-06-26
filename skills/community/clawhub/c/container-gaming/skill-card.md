## Description: <br>
Container-based gaming setup on Linux using Podman, Distrobox, Flatpak gaming apps, Wine/Proton containers, and Sunshine streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverod](https://clawhub.ai/user/silverod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Linux users, and gaming-focused operators use this skill to set up and troubleshoot containerized Linux gaming workflows, Flatpak gaming apps, Wine/Proton launchers, and Sunshine/Moonlight streaming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote installation commands can run privileged code during setup. <br>
Mitigation: Prefer distro or package-manager installation for Distrobox; review any remote script before running it with sudo. <br>
Risk: Unpinned container images can change behavior between runs. <br>
Mitigation: Use trusted container images and pin tags or digests when possible. <br>
Risk: Flatpak and container permissions can expose more host resources than a game requires. <br>
Mitigation: Limit device, filesystem, and socket permissions to the specific game or application need. <br>
Risk: Sunshine and Tailscale serving commands can expose local streaming services to other devices. <br>
Mitigation: Use trusted devices with authentication and ACLs, and stop or disable Sunshine or Tailscale serving when streaming is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silverod/container-gaming) <br>
- [Distrobox install script referenced by skill](https://raw.githubusercontent.com/89luca89/distrobox/main/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Linux-focused operational guidance for local containers, Flatpak applications, Wine/Proton tools, and Sunshine streaming.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
