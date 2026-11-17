## Description:

AI-driven agile development framework with 34+ workflows and 12+ domain expert agents (PM, Architect, Developer, UX, Scrum Master, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansenmemo](https://clawhub.ai/user/hansenmemo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start software projects with AI assistance, follow agile development workflows, and set up AI development environments for BMad Method modules and commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned npm execution, including a non-interactive CI command, which may modify a project directory or run unexpected package versions.

Mitigation: Prefer the pinned installer example or a reviewed lockfile-managed setup, avoid running unpinned commands with sensitive credentials available, and run the installer only in an intended project directory.

## Reference(s):

- [BMad Method Documentation](https://docs.bmad-method.org)
- [BMad Method Discord](https://discord.gg/gk8jAdXWmj)
- [ClawHub Skill Page](https://clawhub.ai/hansenmemo/skills/bmad-method)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose npm installer commands and project setup steps that should be reviewed before execution.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
