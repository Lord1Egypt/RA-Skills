## Description: <br>
Delegates coding tasks to Codex, Claude Code, OpenCode, or Pi agents through PTY-enabled shell sessions for feature work, PR review, refactoring, and iterative code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QCZX0318](https://clawhub.ai/user/QCZX0318) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding implementation, refactoring, PR review, and multi-worktree tasks to local coding-agent CLIs. It is most relevant when the workflow needs PTY-enabled shell execution and background process monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes runnable code that can send user prompts to an undeclared Google Gemini API using an embedded API key. <br>
Mitigation: Remove or replace the embedded API key and disclose the external API path before using the skill with private repositories, secrets, proprietary code, or sensitive prompts. <br>
Risk: Delegated coding-agent workflows may install dependencies, run shell commands, commit, push, create pull requests, or post GitHub comments. <br>
Mitigation: Run agents only in disposable worktrees or tightly scoped directories, avoid unsandboxed modes by default, and manually review dependency installs, commits, pushes, GitHub comments, PR creation, and notification commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QCZX0318/coding-agent-backup-fixed) <br>
- [Publisher profile](https://clawhub.ai/user/QCZX0318) <br>
- [Google Gemini API endpoint used by artifact](https://generativelanguage.googleapis.com/v1/models/gemini-3.1-pro:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a bash-capable environment with PTY support and one of the configured coding-agent CLIs.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
