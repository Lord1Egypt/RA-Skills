## Description:

除秽·调优魄 is a Chinese-language performance optimization skill that helps agents inspect system state, filter noise, tune parameters, clean environments, and report measured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt8899789](https://clawhub.ai/user/lt8899789)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent builders use this skill to diagnose slow systems, identify bottlenecks, propose configuration and parameter tuning, and produce structured optimization reports. It also supports environment cleanup workflows when users explicitly request cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup or tuning suggestions may delete files or change configuration if executed without review.

Mitigation: Ask for diagnostics first, review proposed commands, require confirmation before deletion or configuration changes, and keep backups for important data.

Risk: Performance recommendations may not improve every environment or workload.

Mitigation: Apply changes incrementally, benchmark before and after each change, and continue monitoring after optimization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lt8899789/skills/chu-hui-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown optimization reports with diagnostics, bottleneck analysis, recommendations, executed actions, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed cleanup or tuning commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
