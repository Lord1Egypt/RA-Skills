## Description:

Create, deploy, update, and troubleshoot Coolify applications with the official Coolify CLI. Use when user wants deploy via Coolify, app creation from GitHub, redeploy on push, env vars, logs, or fallback Docker/Traefik routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heldinhow](https://clawhub.ai/user/heldinhow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, redeploy, update, and troubleshoot Coolify-managed applications, including private GitHub deployments, environment variable changes, deployment log review, and fallback Docker or Traefik routing when Coolify app creation is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe infrastructure and credential examples may need review before installation or use.

Mitigation: Review and edit examples before use; require HTTPS and a user-approved Coolify host.

Risk: Tokens could be exposed if placed directly in shell commands.

Mitigation: Avoid putting tokens directly in shell commands; use a safer credential handling method approved by the deployment environment.

Risk: Force redeploys, environment variable changes, direct Docker replacement, or app deletion can affect running infrastructure.

Mitigation: Require explicit user confirmation before taking those actions.

## Reference(s):

- [Coolify Reference](references/coolify-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, CLI examples, Dockerfile snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Coolify CLI commands, Coolify API curl commands, Docker and Traefik fallback commands, deployment checks, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
