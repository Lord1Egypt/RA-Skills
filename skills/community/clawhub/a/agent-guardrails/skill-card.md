## Description: <br>
Agent Guardrails provides mechanical enforcement tools with git hooks, secret detection, deployment verification, and import registries to prevent AI coding agents from bypassing project standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olmmlo-cmd](https://clawhub.ai/user/olmmlo-cmd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to install and apply repository guardrails that catch reimplementation, secret leaks, deployment gaps, and skill update gaps in AI-assisted coding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent repository automation and may modify project files, git hooks, AGENTS.md, and workflow artifacts. <br>
Mitigation: Review the scripts before installation, try them in a test repository first, inspect .git/hooks and AGENTS.md changes, and keep a rollback or uninstall path. <br>
Risk: Unattended commits can occur if AUTO_COMMIT_NO_CONFIRM is intentionally enabled. <br>
Mitigation: Leave AUTO_COMMIT_NO_CONFIRM disabled unless unattended commits are explicitly desired and approved by the team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/olmmlo-cmd/agent-guardrails) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Deployment verification guide](artifact/references/deployment-verification-guide.md) <br>
- [Enforcement research](artifact/references/enforcement-research.md) <br>
- [Skill update feedback](artifact/references/skill-update-feedback.md) <br>
- [AGENTS.md template](artifact/references/agents-md-template.md) <br>
- [Claude Code install guide](artifact/CLAUDE_CODE_INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, shell scripts, and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The provided scripts may create or modify local repository hooks, scripts, AGENTS.md, and workflow files when run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter, skill.json, and changelog list 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
