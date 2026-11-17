## Description:

Audit an LLM evaluation or benchmark repository for integrity and credibility practices across pre-registration, contamination, holdout hygiene, judge validity, statistical honesty, reproducibility, and leaderboard exclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, benchmark maintainers, and reviewers use this skill to audit LLM evaluation repositories before publishing scores, submitting to reviews, or operating public leaderboards. It produces a read-only integrity report with evidence-backed ratings and concrete fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may query GitHub pull request metadata using local gh authentication.

Mitigation: Run it only where read-only PR metadata access is acceptable, or document that PR checks were unavailable if gh access is omitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/eval-integrity)
- [eval-integrity repository](https://github.com/conorbronsdon/eval-integrity)
- [README.md](README.md)
- [Dimension Audit Briefs](patterns/dimension-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit report with file:line evidence, PRESENT/PARTIAL/ABSENT ratings, severity labels, and concrete fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit; may query GitHub pull request metadata through local gh authentication when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
