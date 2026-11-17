## Description:

Runs three AI coding agents in parallel to generate, compare, score, and deliver a selected code solution for a user-provided coding task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiyangzen](https://clawhub.ai/user/weiyangzen)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to run competing AI coding approaches for the same implementation task, collect markdown evaluations and scorecards, and package a final selected solution with comparison rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Final reports may overstate objective winner selection because the authoritative security summary says the delivery script always selects Agent A despite claiming score-based selection.

Mitigation: Review scorecards and comparison reports manually before trusting or publishing the final selected implementation; update the delivery logic to parse and apply actual scores before automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weiyangzen/skills/b3ehive)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [config.yaml](config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, generated workspace files, runnable code artifacts, and shell-command workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates run_a, run_b, run_c, and final workspaces with comparison and decision rationale files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
