## Description:

Review uncertain claims during read-only exploration, then gate a proposed costly or irreversible action under operator policy. Does not choose the mission or execute the action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ales375](https://clawhub.ai/user/ales375)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and agent developers use the skill to review uncertain claims and assess whether the current record supports a proposed costly or irreversible action under operator-approved policy. It can also support read-only exploration without treating a shortlist as permission to act.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or incomplete evidence may produce an unsuitable action recommendation.

Mitigation: Set and approve policy limits yourself, review the full disposition and underlying record, and treat the gate as decision support rather than authorization.

Risk: A stale result or omitted cumulative spending limits could lead to an action beyond the intended bounds.

Mitigation: Require a successful run and fresh output for each review, use a dedicated output path, and enforce cumulative budgets outside this gate.

Risk: Diagnostic output and review files may contain sensitive details.

Mitigation: Keep review files private and restrict access to diagnostic output.

## Reference(s):

- [Credibility Action Gate release](https://clawhub.ai/ales375/skills/credibility-action-gate)
- [Lane contracts](artifact/references/lane_contracts.md)
- [Operator setup](artifact/references/operator-setup.md)
- [Zooidfund review adapter](artifact/references/zooidfund_adapter.md)
- [Zooidfund donor agent operators](https://zooid.fund/donor-agents)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Configuration]

**Output Format:** [JSON disposition report with human-readable review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis-only; does not execute the contemplated action.]

## Skill Version(s):

2.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
