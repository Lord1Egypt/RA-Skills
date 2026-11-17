## Description:

Creates, manages, and opens isolated browser-based code-server development environments using Docker and Cloudflare Tunnel, with Bun, uv, and OpenCode available in the container.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanbasara](https://clawhub.ai/user/lanbasara)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, start, stop, inspect, and delete isolated remote development environments with browser IDE access. It is suited for setting up temporary Docker-backed workspaces, optionally cloning a repository and initializing OpenCode configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser IDEs may be exposed publicly through Cloudflare Quick Tunnel with weak default authentication.

Mitigation: Use strong unique passwords and avoid exposing valuable workspaces through Quick Tunnel until authentication is reviewed and hardened.

Risk: Install and setup paths download external tooling during Docker image builds.

Mitigation: Review installers before use and require pinned, verified installer sources before treating the skill as production-ready.

Risk: Codespace deletion is irreversible and removes local workspace data.

Mitigation: Require explicit deletion confirmation and verify the target codespace name before removing containers or workspace directories.

Risk: Saved passwords and workspace metadata may expose sensitive access details.

Mitigation: Use safer secret handling and review local metadata permissions before using the skill with sensitive repositories.

## Reference(s):

- [Codespace Manager Skill Page](https://clawhub.ai/lanbasara/skills/codespace-manager)
- [Docker installation documentation](https://docs.docker.com/get-docker/)
- [Cloudflare cloudflared downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- [OpenCode configuration schema](https://opencode.ai/config.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Docker containers, local workspace files, Cloudflare Quick Tunnel URLs, and OpenCode configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
