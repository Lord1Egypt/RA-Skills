## Description: <br>
Creates Claude Code slash commands as reusable markdown workflows invoked with /command-name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to create reusable slash commands for repetitive Claude Code workflows, including workflow automation, iterative fixing, delegation, and simple execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated slash commands can later automate powerful actions such as running shell tools, staging or committing code, publishing PRs, or invoking subagents. <br>
Mitigation: Inspect generated command markdown before invoking it and apply extra review to commands that modify code, run shell commands, publish changes, or delegate work. <br>
Risk: Global command installation can make generated workflows available outside the intended project. <br>
Mitigation: Prefer project-local commands unless global behavior is intentionally required. <br>
Risk: Remote installation can pull skill content from an unexpected source. <br>
Mitigation: Verify the remote install source before using the README's npx command. <br>


## Reference(s): <br>
- [Command Patterns](references/patterns.md) <br>
- [Command Best Practices](references/best-practices.md) <br>
- [Command Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown command files with frontmatter, workflow steps, inline shell commands, and usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent command definitions that should be reviewed before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
