## Description: <br>
Deprecated alias for a Claude Code tmux orchestrator that starts observable development sessions, monitors progress, and reports completion back to OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yaxuan42](https://clawhub.ai/user/Yaxuan42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to delegate coding work to Claude Code in tmux sessions, inspect status, and receive completion reports before reviewing changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs long-lived Claude Code jobs with permission prompts disabled and broad shell access. <br>
Mitigation: Use it only in an isolated, backed-up worktree or container where automated file edits and command execution are intended. <br>
Risk: Untrusted labels, paths, SSH hosts, or lint/build commands can affect local or remote shell execution. <br>
Mitigation: Pass only trusted inputs and review task commands, tmux sessions, and completion reports before relying on the results. <br>
Risk: Active tmux sessions may continue running after the user stops watching them. <br>
Mitigation: Monitor task status and stop sessions that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yaxuan42/claude-code-legacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create tmux sessions and local completion report files when its shell scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
