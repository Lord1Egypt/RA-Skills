## Description:

Creates a new AI agent identity by generating SOUL.md, IDENTITY.md, and AGENTS.md and packaging them as a .skill file for ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, configure, package, and optionally publish named agent persona bundles for OpenClaw workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated identity files can overwrite important workspace files and create persistent agent instructions.

Mitigation: Review generated files before installation, back up target workspace files, and copy files only into the intended workspace.

Risk: Persona text and custom slugs have insufficient safeguards for untrusted or unattended workflows.

Mitigation: Use trusted single-line persona inputs, keep custom slugs to simple lowercase hyphen-case names, and avoid unattended publishing or installation until validation is fixed.

Risk: Restarting OpenClaw services can disrupt active sessions.

Mitigation: Restart OpenClaw services only when session interruption is acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/maverick-software/skills/agent-creator)
- [Publisher profile](https://clawhub.ai/user/maverick-software)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with generated workspace files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces identity templates and a packaged .skill archive; publishing and installation steps remain user-controlled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
