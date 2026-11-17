## Description:

Evaluates skill quality, runs automated SKILL.md improvement loops with Pareto-front protection, and tracks score trends across six dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to score agent skills across accuracy, coverage, reliability, efficiency, security, and trigger quality, then optionally apply iterative improvements and track score history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify target skill repositories and create git commits.

Mitigation: Run it only on a disposable copy of trusted skills, review diffs before keeping changes, and avoid running it in repositories where automatic commits are unacceptable.

Risk: The skill can run target test code and documented evaluation commands that may not be read-only.

Mitigation: Use a sandbox with no sensitive environment variables and no network access before evaluating private or third-party skill directories.

Risk: The skill can send SKILL.md content to an external Claude CLI path.

Mitigation: Use --mock when external model calls are not acceptable, especially for private, proprietary, or sensitive skill content.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lanyasheng/skills/auto-improvement-learner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON score reports and improvement summaries, Markdown progress reports, code or file edits, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write memory, state, report, test, reference, and SKILL.md changes in the target skill directory; optional plotting can emit image files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
