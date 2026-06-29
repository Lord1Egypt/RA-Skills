## Description: <br>
Rigorous workflow for software engineering projects that require design documents, API contracts, code review, testing, deployment runbooks, rollback plans, and consistency checks across naming, business logic, and data models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianye](https://clawhub.ai/user/christianye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan and execute multi-module systems, API services, infrastructure changes, and production deployments with explicit design, audit, runbook, and rollback gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included audit script reads local source and configuration files and may print secret-like findings to the terminal. <br>
Mitigation: Review the script and terminal environment before running it, and avoid sharing audit output without checking for sensitive values. <br>
Risk: The workflow can direct agents to run project checks such as TypeScript validation through local tooling. <br>
Mitigation: Run commands only in the intended project workspace after reviewing package scripts and dependency behavior. <br>
Risk: The skill enforces strict process gates that may be excessive for small or read-only tasks. <br>
Mitigation: Use it for multi-module systems, API services, infrastructure work, or deployment changes, and choose a lighter workflow for one-off scripts or read-only analysis. <br>


## Reference(s): <br>
- [Build Protocol Engineering on ClawHub](https://clawhub.ai/christianye/build-protocol-engineering) <br>
- [Engineering Workflow](references/engineering-workflow.md) <br>
- [Design Doc Checklist](references/design-doc-checklist.md) <br>
- [Engineering Audit Script](references/audit-script-engineering.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, document templates, audit instructions, and shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run the included local audit script against a project root.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
