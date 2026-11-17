## Description:

Helps developers connect Claude Code and WorkBuddy to third-party model providers, troubleshoot configuration, and use a local gateway when protocol conversion is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to configure Claude Code or WorkBuddy for third-party models, switch provider profiles, and diagnose connection or response problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing local Claude Code or WorkBuddy settings may overwrite working provider configuration.

Mitigation: Review proposed settings changes and keep a backup before applying them.

Risk: Third-party providers may receive prompts, project context, and credentials sent through configured endpoints.

Mitigation: Check the provider before use and avoid sensitive projects with anonymous or unclear providers.

Risk: The local gateway may write failed request bodies to a local debugging file.

Mitigation: Review local gateway logs and limit access to or remove files containing sensitive request data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/claude-code-third-party-model)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Code]

**Output Format:** [Markdown with configuration and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide edits to local settings and use of a local model gateway.]

## Skill Version(s):

1.3.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
