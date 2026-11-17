## Description:

Coordinates a Coding to Review cycle where one agent implements code changes, another reviews them in read-only mode, and the user decides whether to continue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raccoon-office](https://clawhub.ai/user/raccoon-office)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to coordinate a two-agent coding and review loop for code changes, keeping the reviewer read-only while the main session decides whether to request fixes or finish.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The coder role can modify files in the current workspace when the workflow is invoked.

Mitigation: Run the workflow from the intended workspace and review the coder output and reviewer findings before accepting changes.

Risk: Automatic rounds can repeat coding changes up to the requested round count.

Mitigation: Use a low round count for supervised work and inspect each review decision before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raccoon-office/skills/code-review-cycle-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with structured coder and reviewer sections, plus task prompts and JSON session invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coder diffs, review findings, follow-up decisions, and optional automatic review cycles.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
