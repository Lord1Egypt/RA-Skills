## Description: <br>
Orchestrates multiple Claude Code sessions across projects and lets users monitor status and approve actions through Clawdbot or WhatsApp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yossiovadia](https://clawhub.ai/user/yossiovadia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to delegate long-running coding tasks to Claude Code in tmux sessions, monitor progress, and respond to permission prompts remotely. It is intended for workflows where a Clawdbot assistant coordinates multiple local coding sessions while the user stays in control of approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch Claude Code workers and grant broad unattended approval authority. <br>
Mitigation: Install only for intentional Claude Code orchestration, avoid auto or always approval in sensitive repositories, and review actions before enabling broad approvals. <br>
Risk: Remote approval and monitoring depend on Clawdbot configuration and webhook tokens. <br>
Mitigation: Protect Clawdbot configuration and webhook tokens, and stop the monitor daemon when work is finished. <br>
Risk: The artifact references external GitHub code, while server-resolved import provenance is unavailable. <br>
Mitigation: Verify the external code actually installed and run it in disposable branches or contained worktrees. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yossiovadia/claude-code-wingman) <br>
- [README](artifact/README.md) <br>
- [Usage Guide](artifact/USAGE.md) <br>
- [Helper Library Documentation](artifact/lib/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Claude Code CLI and tmux availability; session actions may depend on user approval posture.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
