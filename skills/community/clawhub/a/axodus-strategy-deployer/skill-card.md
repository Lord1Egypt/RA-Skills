## Description:

Deploy trading strategies with risk gating, monitoring, and guarded live promotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading system operators use this skill to move a strategy from validation into paper deployment and, with explicit approval and controls, guarded live promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed trigger metadata may leave this high-impact live-trading workflow insufficiently scoped.

Mitigation: Install only in environments where invocation can be controlled, keep live trading blocked by default, and require explicit approval, defined risk limits, validated paper results, and a working stop mechanism before any live promotion.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured deployment status, risk limits, and audit event fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify paper or live mode, deployment status, markets, risk limits, audit events, monitoring checklist items, and stop triggers.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
