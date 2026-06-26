## Description: <br>
A comprehensive skill for using the Cursor CLI agent for various software engineering tasks, updated for 2026 features and tmux-based automation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for guidance on installing, authenticating, configuring, and running Cursor CLI workflows for code review, refactoring, debugging, git assistance, and CI-style automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor CLI automation can trust workspaces or apply code changes with insufficient user control. <br>
Mitigation: Use the skill only in trusted repositories, review project rules and MCP configuration first, keep changes version-controlled, and avoid --force unless the results will be reviewed. <br>
Risk: The skill requires SKILLBOSS_API_KEY, which is a sensitive credential. <br>
Mitigation: Provide the key through a secrets manager or scoped environment variable, avoid committing it, and confirm why the key is needed before use. <br>
Risk: The artifact describes tmux-based automation and first-run workspace trust handling. <br>
Mitigation: Do not automate workspace trust; supervise first-run prompts and run automation only after the repository and requested task have been reviewed. <br>


## Reference(s): <br>
- [Cursor CLI install](https://cursor.com/install) <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/abe-cursor-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes interactive and non-interactive Cursor CLI workflows, authentication setup, MCP guidance, and tmux automation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
