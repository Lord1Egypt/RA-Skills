## Description:

Generate production-ready Next.js projects with TypeScript, Tailwind CSS, shadcn/ui, and API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wing8169](https://clawhub.ai/user/wing8169)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scaffold and extend Next.js frontends, including project structure, typed API integration, shadcn/ui components, visual review, environment setup, and deployment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation commands such as npm and npx can run third-party package code during setup.

Mitigation: Review each npm/npx command before execution and use a disposable or well-isolated workspace.

Risk: Optional nginx and sudo setup can expose a local preview externally or change host configuration.

Mitigation: Decline nginx/sudo setup unless external preview access is intentional and the host is prepared for it.

Risk: Screenshot workflows may capture sensitive private or authenticated pages.

Mitigation: Avoid running screenshot capture against private or authenticated content unless the output path and audience are controlled.

Risk: PM2 and process-management commands can affect unrelated services on a shared host.

Mitigation: Use project-specific PM2 names, validate project names before shell use, and avoid broad PM2 or kill commands on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wing8169/skills/frontend-dev)
- [Repository link listed in README](https://github.com/wing8169/openclaw-frontend-dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm/npx commands, PM2 process commands, nginx configuration guidance, environment templates, and screenshot review instructions.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
