## Description:

Cc Coder uses the Claude Code CLI to help automate coding tasks such as creating projects, fixing bugs, implementing features, validating changes, and reporting results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenlavril](https://clawhub.ai/user/wenlavril)

### License/Terms of Use:


## Use Case:

Developers use this skill to delegate routine coding work to Claude Code, including requirements analysis, file changes, syntax checks, web project smoke testing, review loops, and concise completion summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke Claude Code with approval checks skipped.

Mitigation: Run it only in a sandboxed workspace or unprivileged account, and avoid repositories or machines that contain secrets, deployment credentials, or unrelated private files.

Risk: Generated code or shell commands may be incorrect, incomplete, or unsafe for the target project.

Mitigation: Review generated changes before keeping them, run the requested syntax checks or tests, and require manual validation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenlavril/skills/cc-coder)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown status summaries, inline shell commands, and generated or modified project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TASKS.md-style progress tracking and reports task status, change summary, and test conclusions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
