## Description:

Audit an LLM evaluation or benchmark repo for integrity and credibility practices, checking seven benchmark-integrity dimensions and returning a scored report with evidence, severity, and concrete fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, benchmark maintainers, and reviewers use this skill to audit LLM evaluation repositories before publishing or relying on benchmark results. It identifies gaps in pre-registration, contamination control, holdout hygiene, judge validity, statistical reporting, reproducibility, and leaderboard publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect open pull request metadata and diffs through GitHub CLI when available, using the user's existing GitHub session.

Mitigation: Run it only on repositories where that access is acceptable, or use an environment without GitHub CLI access when PR inspection is not desired.

Risk: Parallel subagent audits can be costly or heavy in constrained environments.

Mitigation: Use the documented sequential fallback when parallel execution is too expensive or unavailable.

## Reference(s):

- [README](README.md)
- [Skill workflow](SKILL.md)
- [Dimension audit briefs](patterns/dimension-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with file:line evidence, severity labels, and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit output; may include commands for evidence gathering and guidance for benchmark hardening.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
