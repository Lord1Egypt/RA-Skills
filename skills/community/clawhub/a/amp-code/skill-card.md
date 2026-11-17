## Description:

Delegate coding tasks to Sourcegraph Amp, an autonomous coding agent, for multi-file changes, new features, bug fixes, test writing, or other coding work that benefits from autonomous execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minerva-care](https://clawhub.ai/user/minerva-care)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate substantial coding tasks to Amp in a target project directory, including implementation, refactoring, bug fixes, and test generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Amp with permission checks disabled in a chosen project directory.

Mitigation: Use it only on trusted repositories in a disposable or sandboxed workspace, keep unrelated secrets out of scope, and review diffs plus Amp thread logs before accepting changes.

Risk: Autonomous code changes may be incorrect or incomplete.

Mitigation: Run the relevant tests and review the resulting code before publishing or merging the work.

## Reference(s):

- [Amp Code on ClawHub](https://clawhub.ai/minerva-care/skills/amp-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands, with optional code and configuration changes produced by Amp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the amp binary and may print an Amp thread ID plus the final agent response.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
