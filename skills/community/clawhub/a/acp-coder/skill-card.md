## Description: <br>
Delegate coding tasks to external agents such as Claude Code and Codex through ACP for code changes, analysis, review, testing, debugging, refactoring, and multi-agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiejiesks](https://clawhub.ai/user/jiejiesks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate code analysis, implementation, bug fixing, testing, review, and multi-stage development workflows to configured external coding agents through OpenClaw ACP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes broad persistent OpenClaw security changes, including approve-all permissions, all-session visibility, agent-to-agent access, heartbeat edits, daemon restart, and global npm installation. <br>
Mitigation: Review setup.sh before installation, install only in workspaces where these changes are acceptable, and tighten OpenClaw permissions or triggers for sensitive projects. <br>
Risk: The skill can auto-delegate repository access or edits to configured external coding agents with limited user control. <br>
Mitigation: Use the skill only for repositories that may be exposed to the configured agents, prefer manual invocation for sensitive work, and review generated changes before committing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiejiesks/acp-coder) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with agent orchestration instructions, command examples, and file-writing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May delegate work to configured external coding agents and may result in repository edits, test execution, or configuration changes performed by those agents.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
