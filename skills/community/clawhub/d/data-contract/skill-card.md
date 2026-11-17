## Description:

Defines a data contract between a producer and consumers of a dataset, event, or API, including schema, semantics, quality SLAs, ownership, versioning, breaking-change policy, and change process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers, analytics engineers, API owners, and downstream consumers use this skill to draft explicit data agreements that document schema, field semantics, measurable quality expectations, ownership, versioning, and change governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated data contracts can be incomplete or inaccurate if source schema, ownership, consumer, or SLA details are missing or wrong.

Mitigation: Review the generated contract with producers and affected consumers before relying on it for production change governance.

Risk: Contract drafting may involve sensitive business data, dataset names, schemas, owners, or escalation paths.

Mitigation: Share only the information needed to draft the contract and avoid unnecessary sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/data-contract)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/data-contract.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown data contract with schema table, quality SLAs, ownership, versioning, and change process.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill requests missing asset, producer, consumer, schema, and quality-expectation details before drafting when they are not already provided.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
