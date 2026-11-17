## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for installable skills, compare relevant options, and install skills that extend an agent's capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to run unpinned remote install commands that modify the user's global agent environment.

Mitigation: Inspect skill sources before installation, prefer pinned or preinstalled tooling, avoid confirmation-skipping flags, and use global installs only when future sessions should be affected.

Risk: The skill can steer ordinary help requests toward installing third-party skills.

Mitigation: Confirm that installing an additional skill is necessary and review the selected package before acting on install guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/skills/chen-find-skills)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend or run live skill search and install commands when the user asks to find or install skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
