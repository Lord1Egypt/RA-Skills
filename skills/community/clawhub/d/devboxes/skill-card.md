## Description: <br>
Manage development environment containers (devboxes) with web-accessible VSCode, VNC, and app routing via Traefik or Cloudflare Tunnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adshrc](https://clawhub.ai/user/adshrc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to provision and manage OpenClaw devbox containers with browser-based IDE access, visual desktop access, browser automation, and routable application ports. It supports first-time infrastructure setup, devbox lifecycle tasks, and project setup inside the resulting development environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Docker-backed devbox management and includes host-level Docker socket access guidance. <br>
Mitigation: Install only where an agent is intended to manage containers, and limit Docker access to trusted hosts and users. <br>
Risk: The setup guidance includes world-writable Docker socket or host-path permissions. <br>
Mitigation: Avoid world-writable permissions on shared or sensitive machines; prefer least-privilege host paths and access controls. <br>
Risk: GitHub and Cloudflare tokens may be provided to support private repository cloning and tunnel or DNS setup. <br>
Mitigation: Use scoped tokens, rotate credentials after use when appropriate, and avoid storing broader permissions than the devbox workflow requires. <br>
Risk: VSCode, noVNC, browser automation, and application services can be exposed through configured routing. <br>
Mitigation: Expose IDE and browser services only behind authentication and restrict network access to intended users. <br>


## Reference(s): <br>
- [Project Setup Script Guide](references/setup-script-guide.md) <br>
- [OpenClaw + Traefik Setup Guide](https://gist.github.com/adshrc/3cd9e8a714098f414635b7fe1ab5e573#file-openclaw_traefik-md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce URLs, environment variable values, and setup instructions for Docker-backed devboxes.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
