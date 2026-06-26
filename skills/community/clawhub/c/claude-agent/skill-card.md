## Description: <br>
Claude Agent lets OpenClaw operate Claude Code through tmux and hooks to plan prompts, run coding tasks, handle approvals, monitor completion, and report results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[N1nEmAn](https://clawhub.ai/user/N1nEmAn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to delegate Claude Code coding tasks while OpenClaw manages prompt design, tmux sessions, approval handling, monitoring, and final reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can normalize unattended, high-privilege Claude Code execution when auto-approval or broad permissions are enabled. <br>
Mitigation: Use manual approval for sensitive work, avoid --auto and --dangerously-skip-permissions outside trusted sandboxed projects, and keep Claude Code permissions narrowly scoped. <br>
Risk: Notification and wake payload settings can expose working directories, summaries, or approval details in chat channels if privacy options are relaxed. <br>
Mitigation: Keep event-only notification modes for private code and enable summary or full modes only in trusted private channels. <br>
Risk: Persistent tmux sessions and Claude Code hooks can continue monitoring or waking the agent after a task if not cleaned up. <br>
Mitigation: Review the installed ~/.claude/settings.json hook configuration and use the provided stop script to clean up tmux sessions and monitors. <br>


## Reference(s): <br>
- [ClawHub Claude Agent page](https://clawhub.ai/N1nEmAn/claude-agent) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Claude Code CLI usage](https://docs.anthropic.com/en/docs/claude-code/cli-usage) <br>
- [Claude Code settings](https://docs.anthropic.com/en/docs/claude-code/settings) <br>
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) <br>
- [Claude Code CLI reference](references/claude-code-reference.md) <br>
- [Security and privacy notes](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start or monitor Claude Code sessions through tmux and hooks; users should review permissions, generated changes, and notification settings before relying on results.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and CHANGELOG, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
