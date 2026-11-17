## Description:

Interactive Orchestrix project scaffolding that creates a project directory under ~/Codes/, generates a project brief from Q&A, installs MCP config, hooks, slash commands, tmux scripts, and initializes git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorayo](https://clawhub.ai/user/dorayo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to collect project requirements, scaffold an Orchestrix-enabled workspace, and prepare planning and multi-agent development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent Claude Code hooks and Orchestrix automation into the generated project.

Mitigation: Review the generated .claude settings, hook scripts, and Orchestrix scripts before using the workspace for sensitive work.

Risk: The automation can accept trust or approval prompts during tmux-based agent workflows.

Mitigation: Run the workflow only in repositories where this behavior is intended, and manually review trust or approval prompts when stricter control is needed.

Risk: A real Orchestrix license key may be written into project configuration and could enter git history.

Mitigation: Keep .mcp.json ignored or out of commits, use the placeholder until ready, and rotate any key that was committed accidentally.

## Reference(s):

- [Orchestrix Homepage](https://orchestrix-mcp.youlidao.ai)
- [Create Project on ClawHub](https://clawhub.ai/dorayo/skills/create-project)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with generated project files, shell commands, YAML, JSON, and git configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored from interactive project Q&A and Orchestrix resource templates.]

## Skill Version(s):

3.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
