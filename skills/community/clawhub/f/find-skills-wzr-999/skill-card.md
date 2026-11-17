## Description:

Helps users discover and install agent skills when they ask for installable functionality or ways to extend agent capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawnwangzi](https://clawhub.ai/user/dawnwangzi)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search the open skills ecosystem, compare relevant skills, and install selected skills with the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest unpinned remote CLI commands or global skill installation with confirmations skipped.

Mitigation: Require explicit user approval, prefer pinned CLI and skill versions, install project-locally where possible, and review skill source before execution.

Risk: Search results and installation targets may point to third-party skills with different trust and maintenance profiles.

Mitigation: Review the publisher, source, license, and security posture of each suggested skill before installation.

## Reference(s):

- [Skills ecosystem browser](https://skills.sh/)
- [ClawHub skill page](https://clawhub.ai/dawnwangzi/skills/find-skills-wzr-999)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands for third-party skills that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
