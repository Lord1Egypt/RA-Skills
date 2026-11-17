## Description:

Helps agents design and repair delivery systems across CI/CD pipelines, release and rollback strategy, environments, reliability, incident response, SLOs, capacity, recovery, secrets, and supply chain practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to improve software delivery systems, including pipelines, deployment strategy, rollback planning, environment management, reliability practice, on-call process, and production readiness. It is also used to produce durable operational notes and runbooks for later reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep persistent local operational notes across broad DevOps, infrastructure, ownership, domain, project, and spending records.

Mitigation: Install only when persistent DevOps memory is desired, review the configured paths before use, and constrain local file access where per-task consent is required.

Risk: DevOps work often exposes secrets through pasted pipeline files, environment dumps, logs, Terraform output, or private-key paths.

Mitigation: Store only secret-manager or environment-variable pointers, strip pasted secret values before writing notes, and avoid recording private-key file paths when a managed-secret pointer is available.

Risk: Generated deploy, rollback, migration, infrastructure, or recovery guidance can affect production systems if followed without review.

Mitigation: Review plans before execution, require explicit confirmation for destructive operations, and verify artifact identities, rollback targets, and migration points of no return.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/devops)
- [DevOps Skill Homepage](https://clawic.com/skills/devops)
- [Skill Definition](artifact/SKILL.md)
- [Working File Templates](artifact/memory-template.md)
- [Secrets In The Delivery Path](artifact/secrets.md)
- [Supply Chain](artifact/supply-chain.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code, shell commands, configuration snippets, checklists, plans, and local-note updates when durable outcomes are produced]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local Clawic notes in the configured DevOps, servers, contacts, projects, domains, and finances paths.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
