## Description:

Top-level Linux computer-use skill with a bundled standalone runtime that bootstraps itself without any local Claude installation, private native modules, or extracted app assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to build and run a standalone Linux MCP server for screenshots, mouse and keyboard input, app discovery, window and display mapping, and clipboard operations on a trusted local desktop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots and clipboard access can expose sensitive local information.

Mitigation: Use only on a trusted Linux desktop session, close sensitive windows, and keep sensitive clipboard contents out of view before enabling the skill.

Risk: Broad app, input, clipboard, and system-key permissions can allow unintended desktop actions.

Mitigation: Supervise sessions and prefer releases or configurations that require explicit user approval before screenshots, input, clipboard access, app control, or system-key combinations.

Risk: The runtime reports no native screenshot filtering, so sensitive screen content may be captured if visible.

Mitigation: Rely on MCP-layer gating and keep private applications or documents hidden before requesting screen inspection.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wimi321/skills/computer-use-linux)
- [Skill Instructions](SKILL.md)
- [Project README](project/README.md)
- [MCP Configuration Example](project/examples/mcp-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is Linux-only and assumes a trusted local desktop session.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
