## Description:

Manages development environment containers with web-accessible VSCode, VNC, and app routing via Traefik or Cloudflare Tunnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adshrc](https://clawhub.ai/user/adshrc)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to set up and manage browser-accessible OpenClaw devbox containers for coding, prototyping, frontend debugging, and project setup. It guides onboarding, routing configuration, container spawning, and URL reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup grants broad host and network authority through Docker control, writable host paths, and public devbox URLs.

Mitigation: Install only in a dedicated, non-shared environment where those permissions and exposed URLs are acceptable.

Risk: Docker socket permissions and host path write access can create unsafe defaults.

Mitigation: Avoid chmod 666 on the Docker socket where possible, avoid system-directory host mappings, and use isolated infrastructure.

Risk: VSCode, VNC, Cloudflare, and GitHub tokens may be exposed if public endpoints or broad tokens are used.

Mitigation: Put VSCode and VNC behind authentication, keep tokens narrowly scoped, and rotate or remove tokens that are no longer needed.

Risk: Using mutable container images can make deployments harder to audit.

Mitigation: Prefer pinned image versions or digests before production use.

## Reference(s):

- [Project Setup Script Guide](references/setup-script-guide.md)
- [OpenClaw + Traefik Setup Guide](https://gist.github.com/adshrc/3cd9e8a714098f414635b7fe1ab5e573#file-openclaw_traefik-md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated devbox URLs, Docker and OpenClaw configuration steps, routing setup guidance, and project setup script conventions.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
