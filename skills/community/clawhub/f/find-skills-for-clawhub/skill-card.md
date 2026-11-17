## Description:

Searches for and helps install OpenClaw skills from the ClawHub registry when users ask about available OpenClaw capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrjordandu](https://clawhub.ai/user/mrjordandu)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to search the ClawHub registry, review matching skills, and install selected skills with ClawHub CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes install, update, publish, and sync command paths that can modify local skills or publish local content.

Mitigation: Require explicit user confirmation before install, update, publish, or sync commands, and review each skill before installation.

Risk: The skill allows unpinned npx execution of the ClawHub CLI when a global CLI is not available.

Mitigation: Prefer a pinned and trusted ClawHub CLI version before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrjordandu/skills/find-skills-for-clawhub)
- [ClawHub Website](https://clawhub.ai)
- [ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include skill names, versions, install counts, descriptions, tags, and installation commands when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
