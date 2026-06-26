## Description: <br>
Create Claude Code slash commands as reusable markdown workflows invoked with /command-name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a2mus](https://clawhub.ai/user/a2mus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create project-local or global Claude Code slash commands for repeatable workflows. It guides command naming, argument design, workflow structure, file creation, and optional testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated slash commands can persist in project or global command directories and may affect future agent behavior. <br>
Mitigation: Prefer project-local commands unless global reuse is intentional, and inspect generated markdown before saving or invoking it. <br>
Risk: Commands that edit files, stage or commit changes, publish pull requests, deploy, or run broad shell automation can perform high-impact actions. <br>
Mitigation: Add explicit confirmation steps to generated commands before high-impact actions. <br>


## Reference(s): <br>
- [Command Best Practices](references/best-practices.md) <br>
- [Command Examples](references/examples.md) <br>
- [Command Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command frontmatter, workflow steps, and inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent slash-command files for Claude Code when the user approves file creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
