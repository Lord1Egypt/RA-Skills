## Description: <br>
Controls and manages the Claude Code coding assistant for project-aware coding, code review, refactoring, debugging, documentation, and feature implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RocherKong](https://clawhub.ai/user/RocherKong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to launch or configure Claude Code for software development tasks such as feature work, code review, refactoring, debugging, and project documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The launcher can grant Claude Code broad read, write, edit, and shell access in the selected project. <br>
Mitigation: Review or replace `.claude/settings.json` before use, restrict allowed tools and directories, and prefer approval-based permission modes for sensitive repositories. <br>
Risk: The included launcher creates a permissive default project configuration automatically. <br>
Mitigation: Inspect generated `.claude/settings.json` before running tasks and adjust `allowedTools`, `maxTurns`, and `permissionMode` to match the project risk level. <br>
Risk: The artifact claims isolated ACP execution, but the included files do not substantiate that isolation behavior. <br>
Mitigation: Do not rely on isolation claims alone; run the skill only in contained workspaces with a clear plan for secrets, repository access, and generated changes. <br>


## Reference(s): <br>
- [Claude Code Documentation](https://docs.anthropic.com/claude-code) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Claude Code Configuration Reference](references/config-reference.md) <br>
- [Claude Code Workflow Reference](references/workflows.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/RocherKong/claudecode-controller) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch Claude Code with broad project read, write, edit, and shell permissions depending on local configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
