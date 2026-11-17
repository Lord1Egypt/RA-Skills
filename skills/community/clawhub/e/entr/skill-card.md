## Description:

Run arbitrary commands when files change. Useful for watching files and triggering builds or tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ask an agent for entr-based watch workflows that rerun builds, tests, or long-running processes when files change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: entr can run arbitrary commands, including shell-evaluated commands with -s.

Mitigation: Treat watched directories and commands as trusted input and review generated entr invocations before execution.

Risk: entr blocks the terminal and watch processes can keep running in the background.

Mitigation: Run watch sessions deliberately and stop any background watch process after the task is complete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
