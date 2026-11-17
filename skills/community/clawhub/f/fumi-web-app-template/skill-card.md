## Description:

OpenClaw workspace template for web application development, with guidance for user experience, responsive design, and performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirofumiko](https://clawhub.ai/user/hirofumiko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to set up an OpenClaw web application workspace with reusable templates for identity, operating rules, user preferences, memory, and monitoring. It supports full-stack web app work across UX design, frontend and backend development, APIs, testing, deployment, performance, security, accessibility, and SEO.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The template encourages broad autonomous memory, bootstrap, and heartbeat behavior that may exceed a simple development template.

Mitigation: Review and edit templates/AGENTS.md before use, especially BOOTSTRAP.md handling, memory files, heartbeat behavior, and instructions that allow action without asking.

Risk: Proactive monitoring and maintenance guidance may lead an agent to inspect logs, scan results, dependency status, or project state unexpectedly.

Mitigation: Limit heartbeat behavior to approved checks and require confirmation before accessing sensitive logs, changing dependencies, deploying, or taking action outside the workspace.

Risk: Workspace memory files can contain personal or project-sensitive context.

Mitigation: Keep long-term memory out of shared contexts and remove secrets or private data from MEMORY.md and daily notes before sharing the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirofumiko/skills/fumi-web-app-template)
- [Publisher profile](https://clawhub.ai/user/hirofumiko)
- [README.md](artifact/README.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [AGENTS.md template](artifact/templates/AGENTS.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown workspace templates with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable OpenClaw workspace files such as SOUL.md, IDENTITY.md, AGENTS.md, USER.md, and HEARTBEAT.md.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, and CHANGELOG.md released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
