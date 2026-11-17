## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyserkazi1](https://clawhub.ai/user/keyserkazi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find installable skills for specialized tasks, compare relevant options, and receive installation commands when they want to extend an agent's capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run unpinned package-manager commands or install third-party skills globally.

Mitigation: Use a pinned, trusted Skills CLI version, review the exact skill source before installation, and avoid global skipped-prompt installs unless explicitly intended.

Risk: Broad triggering can turn general capability questions into third-party skill installation recommendations with limited safety checks.

Mitigation: Require explicit user confirmation for each install and review recommended packages before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyserkazi1/skills/find-skillsnow)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline bash code blocks and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend package-manager commands for discovering, adding, checking, and updating skills.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
