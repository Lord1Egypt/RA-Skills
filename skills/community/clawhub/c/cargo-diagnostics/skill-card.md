## Description:

Diagnoses Cargo runs and batches by tracing execution paths, grouping failures, and attributing workflow credit use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to explain failed or unexpected Cargo runs, find common causes across batches, and understand where workflow credits are spent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support reports may include sensitive run information.

Mitigation: Review and redact support reports before submission.

Risk: Connector changes, deployments, and paid pilots or reruns can have operational or billing impact.

Mitigation: Require approval before connector changes, deployments, and every paid pilot or rerun.

## Reference(s):

- [Run trace guide](references/run-trace.md)
- [Batch error sweep guide](references/batch-error-sweep.md)
- [Play cost profile guide](references/play-optimize-credits.md)
- [Cargo skills project homepage](https://github.com/getcargohq/cargo-skills)
- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/cargo-diagnostics)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with compact tables, execution paths, and inline shell or SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include grouped error causes and credit estimates; the skill documents diagnostic steps rather than exporting bulk data.]

## Skill Version(s):

1.6.1 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
