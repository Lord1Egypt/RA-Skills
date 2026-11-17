## Description:

ClawLite Investigate is a multilingual debugging workflow that guides agents through root-cause investigation, pattern analysis, hypothesis validation, focused implementation, and verification reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to investigate bugs, verify root-cause hypotheses, make narrowly scoped fixes, and report reproducible evidence before closing a debugging task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read relevant project files, run tests, and make code fixes during debugging.

Mitigation: Review the proposed diff, keep fixes narrowly scoped, and require test evidence before deploying changes.

Risk: The workflow is primarily written in Chinese, which can reduce reviewer clarity for non-Chinese users.

Mitigation: Translate or review the instructions before relying on the workflow in multilingual teams.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown debug reports with inline shell commands and code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include root-cause hypotheses, verification evidence, regression test notes, and DONE/DONE_WITH_CONCERNS/BLOCKED status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
