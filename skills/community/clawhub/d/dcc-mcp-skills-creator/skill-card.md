## Description:

Create, edit or validate DCC-MCP tool skill packages (SKILL.md and tools.yaml). Use dcc-mcp-creator for complete adapter repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold, edit, and validate DCC-MCP tool skill packages, including their SKILL.md instructions, tools.yaml declarations, and supporting scripts. Use it for package-level skill work; full adapter repositories are handled by dcc-mcp-creator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or edited skill packages may contain behavior that has not been reviewed.

Mitigation: Review the package contents before loading the skill.

Risk: A separate installation can introduce unreviewed source changes or runtime prerequisites.

Mitigation: Install from an independently reviewed commit and review runtime prerequisites separately.

Risk: Optional task statistics may expose information outside the relevant task context.

Mitigation: Limit statistics review to the relevant session and omit secrets.

## Reference(s):

- [Project skill page](https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp-skills-creator/SKILL.md)
- [Authoring workflow](artifact/references/AUTHORING_WORKFLOW.md)
- [Tool runtime contract](artifact/references/TOOL_RUNTIME_CONTRACT.md)
- [Package validation](artifact/references/PACKAGE_VALIDATION.md)
- [Verified install procedure](artifact/references/VERIFIED_INSTALL.md)

## Skill Output:

**Output Type(s):** [Files, Code, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown instructions, YAML configuration, Python scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or edits skill package files and provides validation guidance.]

## Skill Version(s):

0.19.117 (source: SKILL.md frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
