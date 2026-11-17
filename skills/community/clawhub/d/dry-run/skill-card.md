## Description:

Dry Run helps agents simulate workflows, migrations, bulk updates, automations, or other side-effecting operations before committing changes when effects are broad, costly, irreversible, externally visible, or difficult to audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to preview side-effecting actions, compare predicted outcomes with invariants, and decide whether to approve, revise, or reject live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dry-run reports can include customer records, messages, or other sensitive business details.

Mitigation: Review reports carefully and handle them with the same access controls and retention expectations as the underlying business data.

Risk: A dry-run setup that still sends real notifications or writes production data can create unintended side effects.

Mitigation: Block or redirect writes and external delivery paths before simulation, then make any side effects that cannot be simulated faithfully explicit in the report.

## Reference(s):

- [Overpowered suite](https://github.com/raguets/overpowered)
- [ClawHub skill page](https://clawhub.ai/raguets/skills/dry-run)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown dry-run report with scope, predicted changes, exceptions, human gates, invariant checks, and a go/no-go recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend skipping full dry-run ceremony for trivially reversible, low-risk actions.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
