## Description: <br>
Orchestrates a five-reviewer code review over a git diff, pull request diff, patch, or commit range, then produces one consolidated report for follow-up implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincent-ng](https://clawhub.ai/user/vincent-ng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate focused code review across correctness, architecture, testability, readability, and simplicity concerns, then merge the findings into one actionable report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nested review may run with broader filesystem authority than a review helper typically needs. <br>
Mitigation: Review privilege defaults before installing and prefer --no-yolo or AUTOREVIEW_YOLO=0 for normal use. <br>
Risk: Private diffs may be exposed to fallback reviewers if automatic fallback behavior is enabled. <br>
Mitigation: Disable automatic fallback reviewers when reviewing private or sensitive changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vincent-ng/five-star-reviewers) <br>
- [diff-acquisition.md](references/diff-acquisition.md) <br>
- [report-template.md](references/report-template.md) <br>
- [review-protocol.md](references/review-protocol.md) <br>
- [reviewer-rubric.md](references/reviewer-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review reports with prioritized findings and suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write five reviewer reports and one consolidated report under docs/five-star-reviewers when the agent environment permits file writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
