## Description: <br>
Claude Code Pro helps agents run and manage token-efficient Claude Code tasks in isolated tmux sessions with completion callbacks, smart dispatch guidance, and structured monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill to delegate larger multi-file coding tasks to a background Claude Code session, monitor progress only when needed, and clean up local sessions after completion. It is intended for trusted local worktrees where tmux, bash, and the Claude CLI are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto mode starts Claude Code with permission prompts skipped, allowing the background process to act as the local user in the selected worktree. <br>
Mitigation: Prefer plan mode when possible, run only in trusted version-controlled worktrees, and avoid sensitive directories. <br>
Risk: Persistent tmux sessions can continue running after the agent stops watching them. <br>
Mitigation: Use the list and monitor commands to check active sessions, then stop individual sessions or all sessions when work is complete. <br>
Risk: Completion callbacks and captured terminal output can be incomplete or misleading if the underlying task fails or reports completion too early. <br>
Mitigation: Review session output before trusting completion callbacks and verify generated code or file changes before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swaylq/claude-code-pro) <br>
- [Publisher profile](https://clawhub.ai/user/swaylq) <br>
- [Voidborne project site](https://voidborne.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON session status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux, bash, and the claude CLI; session monitoring can return captured terminal output from local Claude Code processes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
