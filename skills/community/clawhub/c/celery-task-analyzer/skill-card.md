## Description:

Analyze Celery task configurations for reliability, performance, and debugging across retry policies, routing, serialization, result backends, worker settings, beat schedules, and task design patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Celery applications for task reliability, queue routing, serialization safety, result backend configuration, worker tuning, beat scheduling, and remediation steps before production changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read Celery project files, logs, or metrics that include private application or infrastructure details.

Mitigation: Point the agent only at the intended project scope and redact unrelated private code, secrets, logs, or metrics before sharing inputs.

Risk: Remediation snippets and configuration recommendations could change task delivery, retry, routing, or worker behavior if applied without review.

Mitigation: Review proposed changes with the owning engineering team and validate them in staging before applying them to production Celery deployments.

## Reference(s):

- [Celery Task Analyzer - ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/celery-task-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prioritized findings, health scoring, Celery configuration recommendations, and remediation examples.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
