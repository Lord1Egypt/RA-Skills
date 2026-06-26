## Description: <br>
Integrates OpenClaw with Claude Code CLI so an agent can read codebases, edit files, run commands, review code, debug issues, and automate coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-11even](https://clawhub.ai/user/mr-11even) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to invoke Claude Code from OpenClaw for codebase exploration, implementation tasks, tests, code review, debugging, session management, and scripted CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claude Code use through OpenClaw can lead to project file edits or terminal command execution. <br>
Mitigation: Use least-privilege credentials, work on a branch or sandbox, and review commands and diffs before accepting changes. <br>
Risk: Credentials and trusted integrations can be exposed through installer choices, prompts, MCP servers, hooks, or sub-agent configurations. <br>
Mitigation: Verify the Claude installer source, avoid pasting secrets, and connect only MCP servers, hooks, and sub-agents that are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mr-11even/claude-code-openclaw-skill) <br>
- [Claude Code hooks documentation](https://code.claude.com/docs/en/hooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; Claude Code invocations may return text, JSON, stream JSON, code changes, or shell output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can drive coding actions through Claude Code CLI, so users should review commands, diffs, and generated changes before accepting them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
