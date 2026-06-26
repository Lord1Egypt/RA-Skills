## Description: <br>
ClawGator Superpowers provides a complete software development workflow for brainstorming, planning, systematic execution, test-driven development, debugging, code review, and git worktrees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renggap](https://clawhub.ai/user/renggap) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide software changes through brainstorming, planning, isolated git worktrees, TDD, debugging, code review, and final verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad automatic influence over development sessions and can steer major code changes before implementation. <br>
Mitigation: Review the activation rules and keep human approval checkpoints before enabling it in important repositories. <br>
Risk: The skill can propose repo-changing commands, worktree setup, dependency installation, build or test commands, and branch finishing actions. <br>
Mitigation: Inspect commands before execution, run them in isolated worktrees when possible, and require verification output before merge or release actions. <br>
Risk: The startup hook and project-controlled workflow files can affect agent behavior with limited confirmation. <br>
Mitigation: Review hooks, plugin configuration, and skill files before installation or updates. <br>


## Reference(s): <br>
- [ClawGator Superpowers on ClawHub](https://clawhub.ai/renggap/clawgator-superpowers) <br>
- [README.md](README.md) <br>
- [OpenClaw Plugin Manifest](openclaw.plugin.json) <br>
- [Testing Superpowers Skills](docs/testing.md) <br>
- [Superpowers for Codex](docs/README.codex.md) <br>
- [Superpowers for OpenCode](docs/README.opencode.md) <br>
- [obra/superpowers](https://github.com/obra/superpowers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce plans, design notes, review feedback, debugging hypotheses, verification steps, and repository-changing command suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, openclaw.plugin.json, README.md, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
