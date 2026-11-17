## Description:

Helps users discover and install agent skills when they ask for specialized capabilities or ways to extend an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin797860](https://clawhub.ai/user/robin797860)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to discover installable skills for specialized tasks, compare relevant options, and optionally install a selected skill using the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes unpinned remote CLI execution and non-interactive global installation of third-party skills.

Mitigation: Review the source and version of any skill before installing it, prefer pinned CLI and skill versions, avoid non-interactive installs, and use global installation only when persistence across sessions is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robin797860/skills/find-skills-robin)
- [Skills CLI catalog](https://skills.sh/)
- [Example skill listing](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Skills CLI search and installation commands for third-party skills.]

## Skill Version(s):

0.1.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
