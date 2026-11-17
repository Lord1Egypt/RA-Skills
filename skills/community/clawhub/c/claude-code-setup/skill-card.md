## Description:

Sets up a production-grade .claude/ AI collaboration layer for projects using Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eaveluo](https://clawhub.ai/user/eaveluo)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to bootstrap and supervise project-level Claude Code configuration, including project instructions, rule files, context files, reusable prompts, and project-private skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause an agent to create persistent .claude/ configuration files when the user did not clearly ask for setup.

Mitigation: Invoke the skill only for explicit Claude Code setup work or after confirming that persistent project instructions are wanted.

Risk: Generated CLAUDE.md, rules, context, skills, and prompt files can influence later agent behavior in the project.

Mitigation: Review generated .claude/ files before future development work and edit or remove guidance that does not match the project.

Risk: Running setup in the wrong directory can place .claude/ configuration in a workspace root instead of the intended project.

Mitigation: Confirm the target project directory before running setup and create .claude/ only inside that project.

Risk: Force mode can replace existing generated files in an established .claude/ directory.

Mitigation: Avoid force mode unless overwriting existing Claude Code configuration is intentional and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eaveluo/skills/claude-code-setup)
- [Publisher profile](https://clawhub.ai/user/eaveluo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets and generated project configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates .claude/ project files and skips an existing nonempty .claude/ directory unless force mode is used.]

## Skill Version(s):

1.0.1 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
