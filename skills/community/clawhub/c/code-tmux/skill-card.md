## Description: <br>
Run coding tasks in persistent tmux sessions with git worktree isolation, supporting Claude Code, Codex, CodeBuddy, OpenCode, and other interactive coding-agent CLIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanshenstarto](https://clawhub.ai/user/yuanshenstarto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to delegate build, fix, refactor, and review tasks to a chosen coding agent while isolating each task in a git worktree and keeping the session persistent in tmux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates coding work to high-privilege agent CLIs and includes permission-skipping examples. <br>
Mitigation: Review commands before execution and remove permission-skipping flags unless the user intentionally accepts that access. <br>
Risk: Symlinking full environment files into worktrees can expose secrets to spawned agents. <br>
Mitigation: Link only the environment files needed for the task and avoid exposing full .env files when narrower credentials are sufficient. <br>
Risk: Incorrect tmux session names or worktree paths can lead to cleanup or commands affecting the wrong workspace. <br>
Mitigation: Verify exact session names and worktree paths before sending commands or removing sessions and worktrees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanshenstarto/code-tmux) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [tmux](https://github.com/tmux/tmux) <br>
- [Claude Code](https://github.com/anthropics/claude-code) <br>
- [Codex](https://github.com/openai/codex) <br>
- [OpenCode](https://github.com/sst/opencode) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs and monitors persistent tmux sessions and relays plans, questions, and status back to the user.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
