## Description:

Builds a traceable ledger from agent action logs and flags operations that bypassed a gate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and compliance teams use the skill to review explicitly selected agent action logs, build a timestamped ledger, and identify operations its gate check flags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean report can miss unauthorized writes and should not be treated as proof that all actions were authorized.

Mitigation: Review the selected log and relevant permissions independently before relying on the report for compliance or access decisions.

Risk: Action logs may contain sensitive information, and following links outside the selected log could expose unrelated data.

Mitigation: Use only explicitly selected, redacted log files and avoid symlinks.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/agent-trace-audit)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain-text timestamped action ledger and violation summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints ledger entries and a count of flagged ungated writes; a clean result does not establish that actions were authorized.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
