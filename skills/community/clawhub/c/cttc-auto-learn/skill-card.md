## Description:

Cttc Auto Learn helps an agent set up and run browser automation for mooc.ctt.cn learning workflows, including study-hour, topic, course, and task modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gandli](https://clawhub.ai/user/gandli)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate mooc.ctt.cn course playback, login handling, progress monitoring, and status reporting for learning-hour workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may violate training-platform rules by automating course completion and simulating presence.

Mitigation: Use only with explicit authorization from the account owner and platform or organization responsible for the training workflow.

Risk: The skill executes unpinned third-party code.

Mitigation: Review the source code, pin it to a trusted revision, and run it in a restricted environment before using it with real accounts.

Risk: The skill stores reusable login state locally.

Mitigation: Use a dedicated browser profile or isolated environment and protect or delete generated authentication files after use.

Risk: Browser automation and process cleanup may disrupt existing browser sessions.

Mitigation: Run the workflow on a dedicated machine, VM, or disposable browser profile that does not hold unrelated active sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gandli/skills/cttc-auto-learn)
- [Project URL](https://github.com/gandli/cttc-auto-learn)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown instructions with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+, uv, Playwright, and access to mooc.ctt.cn; execution may create local authentication, QR code, log, and status files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
