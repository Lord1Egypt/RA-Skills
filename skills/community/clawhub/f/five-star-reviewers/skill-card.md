## Description:

Five Star Reviewers runs a coordinated, language-agnostic code review over a git diff, pull request diff, patch, or commit range by launching five focused reviewer agents and producing a consolidated Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-ng](https://clawhub.ai/user/vincent-ng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review repository changes through five focused reviewer perspectives and produce an actionable consolidated report for a human or follow-up AI implementation pass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect repository context beyond the initial diff to judge behavior, module boundaries, or tests.

Mitigation: Run it only in repositories whose code may be reviewed by the active agent environment.

Risk: Generated review guidance can be incomplete or mistaken, especially on large or ambiguous diffs.

Mitigation: Have a human reviewer check the consolidated report before using it as implementation direction.

Risk: The workflow writes Markdown reports under docs/five-star-reviewers when file writes are available.

Mitigation: Review those generated files before committing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincent-ng/skills/five-star-reviewers)
- [Diff acquisition](references/diff-acquisition.md)
- [Report template](references/report-template.md)
- [Review protocol](references/review-protocol.md)
- [Reviewer rubric](references/reviewer-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes five reviewer reports and one consolidated report under docs/five-star-reviewers when file writes are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
