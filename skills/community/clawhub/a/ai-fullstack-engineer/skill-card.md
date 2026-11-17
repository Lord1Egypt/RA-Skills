## Description:

Provides an AI-assisted full-stack web development toolkit covering API and database design, backend and frontend implementation, browser debugging, performance, and application scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

Developers and small teams use this skill to plan and build web applications across APIs, databases, backends, frontends, browser automation, and performance. It provides routed playbooks, reusable templates, and scripts for scaffolding applications and generating TypeScript types from OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious, citing a PostgreSQL configuration exposed on all host interfaces with fixed superuser credentials, along with installation and workflow risks; scan coverage is incomplete.

Mitigation: Before installing, review the PostgreSQL configuration and unpinned installation commands, check how the host runtime limits the skill's access, and account for unresolved references in the incomplete scan coverage.

## Reference(s):

- [Full-Stack Workflow](references/fullstack-workflow.md)
- [Backend Playbook](references/backend-playbook.md)
- [Frontend Playbook](references/frontend-playbook.md)
- [Next.js App Router Playbook](references/nextjs-app-router-playbook.md)
- [Tailwind Audit Playbook](references/tailwind-audit-playbook.md)
- [Multi-Agent Orchestration Playbook](references/multi-agent-orchestration-playbook.md)
- [Browser Operations Playbook](skills/browser-ops/references/browser-ops-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code examples, shell commands, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can generate application scaffold files and TypeScript types from OpenAPI specifications.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
