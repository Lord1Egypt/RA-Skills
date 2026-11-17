## Description:

Agent发布技能 helps agents prepare versioned skill packages and coordinate confirmed publishing or pushing updates to ClawHub and GitHub when core agent files change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to detect changes in core agent files, prepare a versioned skill package, and coordinate publication to ClawHub or GitHub with confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may package complete agent configuration files that contain secrets, private endpoints, internal instructions, customer data, or credentials.

Mitigation: Review the exact packaged files before installation or use, apply explicit file allowlists, and run secret scanning before any publication step.

Risk: The skill can push packaged content to public external destinations such as ClawHub or GitHub.

Mitigation: Prefer private repositories when appropriate and require separate confirmations for ClawHub publishing, GitHub pushing, and public visibility.

Risk: Generated skill directories can include broader agent context than intended for a release.

Mitigation: Exclude private instructions, customer data, internal endpoints, and credentials from SOUL.md, AGENTS.md, IDENTITY.md, TOOLS.md, and generated skill directories before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/perrykono-debug/skills/agent-publish)
- [Packaged Skill Definition](artifact/SKILL.md)
- [Packaged Release Metadata](artifact/_meta.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a packaged skill directory and publish to external services when executed with user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
