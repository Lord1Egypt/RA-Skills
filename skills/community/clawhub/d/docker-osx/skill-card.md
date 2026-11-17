## Description:

Run macOS in Docker on Linux with KVM for iOS app builds and macOS-only software workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nightvibes3](https://clawhub.ai/user/nightvibes3)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start, stop, inspect, and connect to a Docker-hosted macOS VM on Linux hosts with KVM support, especially for iOS build and macOS-only software workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starts a high-trust macOS VM container with Docker and KVM access.

Mitigation: Install only on a dedicated, trusted Linux host where Docker and KVM use are acceptable.

Risk: SSH and VNC can expose access to the VM if reachable from untrusted networks.

Mitigation: Bind SSH and VNC to localhost or restrict access with firewall rules.

Risk: Uses weak default VM credentials.

Mitigation: Change or disable the default password before use.

Risk: The Docker image reference is not pinned to a reviewed digest.

Mitigation: Prefer a reviewed and pinned Docker-OSX image digest.

Risk: The Docker install shortcut uses a curl-to-shell pattern.

Mitigation: Avoid the curl-to-shell Docker install shortcut and use a reviewed installation path.

Risk: Stopping the VM removes the container rather than only pausing it.

Mitigation: Treat the stop command as container removal and preserve needed state outside the container.

## Reference(s):

- [Docker-OSX project](https://github.com/sickcodes/Docker-OSX)
- [ClawHub skill page](https://clawhub.ai/nightvibes3/skills/docker-osx)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-style command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker and KVM; exposes SSH and VNC connection details for the VM.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
