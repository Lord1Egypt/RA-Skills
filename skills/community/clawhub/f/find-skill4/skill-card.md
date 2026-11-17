## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzmmmeee](https://clawhub.ai/user/zzzmmmeee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover relevant installable skills, compare quality signals, and install vetted skills when extending an agent's capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned remote Skills CLI commands and includes a global install command that skips prompts.

Mitigation: Review target skill source before installing, prefer a pinned and locally vetted Skills CLI, and avoid global or prompt-skipping installs unless persistent global installation is intentional.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zzzmmmeee/skills/find-skill4)
- [Skills Directory and Leaderboard](https://skills.sh/)
- [Example Skills Directory Listing](https://skills.sh/vercel-labs/agent-skills/react-best-practices)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands and external skill links; users should vet sources before executing commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
