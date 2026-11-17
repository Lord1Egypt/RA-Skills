## Description:

Caveman Review produces ultra-compressed, actionable code review comments with exact locations, problems, and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill during PR review to produce paste-ready, terse findings with exact line references, concrete problems, and direct fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terse review mode can omit context needed for security findings, architectural disagreements, or onboarding.

Mitigation: Use normal review style for those cases and include fuller rationale or references before resuming terse comments.

Risk: The skill may activate during pull request reviews when normal review prose is expected.

Mitigation: Say "stop caveman-review" or "normal mode" to return to verbose review style.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seanford/skills/caveman-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-ready one-line code review comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paste-ready PR review findings; no code changes, approval decisions, or command execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
