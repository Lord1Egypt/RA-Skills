## Description:

Helps users discover and install agent skills for specialized tasks through Skills CLI search and installation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianjin-ren](https://clawhub.ai/user/tianjin-ren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify relevant installable skills for a requested task, present options, and optionally provide Skills CLI install commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned Skills CLI commands and a global install pattern that skips confirmations.

Mitigation: Review publishers and repositories before installation, avoid the -g and -y install pattern by default, and prefer pinned or reviewed CLI and skill versions.

Risk: Skill discovery and update guidance can lead to installs or bulk updates without inspecting what will change.

Mitigation: Inspect candidate packages, publishers, repositories, and proposed updates before running install or update commands.

## Reference(s):

- [Skills CLI Catalog](https://skills.sh/)
- [ClawHub Skill Page](https://clawhub.ai/tianjin-ren/skills/find-skills-tianjin)
- [Publisher Profile](https://clawhub.ai/user/tianjin-ren)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown text with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested Skills CLI search, install, check, or update commands.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
