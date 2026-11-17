## Description:

Helps users discover and install agent skills when they ask for specialized capabilities or express interest in extending agent functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlylingo9817-sys](https://clawhub.ai/user/onlylingo9817-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find relevant installable skills, present candidate skill options, and optionally install a selected skill with the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage global or unattended skill installation, which can permanently change the user's agent environment.

Mitigation: Require user confirmation before installing or updating skills, avoid skipped-confirmation installs by default, and review the selected skill source before adding it.

Risk: Broad skill discovery can surface untrusted or unpinned packages.

Mitigation: Prefer trusted publishers or pinned versions and verify the package source before executing installation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlylingo9817-sys/skills/find-skills-bak)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with Skills CLI commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install or update skills; user confirmation is recommended before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
