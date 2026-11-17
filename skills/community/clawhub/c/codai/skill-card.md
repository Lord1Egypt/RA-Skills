## Description:

Orchestration skill for the codai-dev local environment. Routes user commands to the right plugin (proxy-manager, mysql-manager, postgres-manager, redis-manager, worktree-manager). Use when the user asks to manage any part of the dev environment without specifying which plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Codai to orchestrate the codai-dev local development environment, including starting services, routing worktree requests, checking status, and selecting the correct database, proxy, Redis, PostgreSQL, or worktree command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers such as `codai` and generic start phrases can route ordinary user requests into local infrastructure actions.

Mitigation: Review and narrow triggers before installing, and require explicit user intent before starting, stopping, or modifying local services.

Risk: The documented default MySQL root password is weak.

Mitigation: Require a unique MySQL root secret and keep database access bound to trusted local or Docker networks.

Risk: Worktree removal, Redis flush, and database dump operations are destructive or high-impact.

Mitigation: Require explicit confirmation and preserve source databases such as `codai_main` before running these commands.

## Reference(s):

- [ClawHub Codai Skill](https://clawhub.ai/pereirajair/skills/codai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes local development requests to Docker- and Git-based service, database, proxy, and worktree operations.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
