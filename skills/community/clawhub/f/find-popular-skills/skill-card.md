## Description:

Discover and install the best agent skills from skills.sh (1.9M+ ecosystem) and ClawHub. Find top skills by category, check leaderboards, verify quality, extract SKILL.md, and publish to ClawHub. Use when user asks 'find a skill for X', 'how do I do X', or wants to extend agent capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find, assess, install, adapt, and publish agent skills from skills.sh and ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad install and publish guidance could lead an agent to install or publish skills without enough scoping or consent.

Mitigation: Review the skill before installation, verify exact package and skill versions, and require explicit user approval before running install or publish commands.

Risk: Command examples using global installation flags or command-line tokens can create shell-history, environment, and remote-publication risks.

Mitigation: Avoid running `-g -y` examples as-is, do not pass real tokens on the command line, and use approved credential handling for ClawHub authentication.

## Reference(s):

- [skills.sh](https://skills.sh)
- [ClawHub skill page](https://clawhub.ai/maliot100x/skills/find-popular-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/maliot100x)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference curl, npx skills, and clawhub CLI commands; review commands before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
