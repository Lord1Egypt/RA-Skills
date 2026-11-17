## Description:

Guides agents through disciplined software engineering projects with design documents, API contracts, consistency audits, deployment runbooks, and rollback plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianye](https://clawhub.ai/user/christianye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan, implement, review, audit, and deploy multi-module software systems where API contracts, data consistency, runbooks, and rollback plans matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit script can run unpinned npx code in a project checkout.

Mitigation: Run the script only in a sandboxed checkout with minimal environment variables, and prefer a pinned local TypeScript compiler or local-only npx mode for sensitive repositories.

Risk: The skill can influence code, deployment, and rollback decisions for production systems.

Mitigation: Require independent review, run the audit checks before deployment, and verify runbook and rollback steps before execution.

## Reference(s):

- [Engineering Workflow](references/engineering-workflow.md)
- [Design Doc Checklist](references/design-doc-checklist.md)
- [Engineering Audit Script](references/audit-script-engineering.sh)
- [ClawHub Skill Page](https://clawhub.ai/christianye/skills/build-protocol-engineering)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with checklists, code snippets, shell commands, and structured engineering documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce requirements notes, D1-DN design documents, API contracts, audit findings, deployment runbooks, rollback plans, and checklist results.]

## Skill Version(s):

1.0.1 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
