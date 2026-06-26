## Description: <br>
Provides guidance for delegating coding work to terminal-based agents through PTY-enabled shell commands and background sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QCZX0318](https://clawhub.ai/user/QCZX0318) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate coding agents for feature work, refactoring, PR review, and parallel worktree tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that prompts may be sent to Google Gemini through an embedded credential. <br>
Mitigation: Remove or replace the embedded key before use, avoid sensitive prompts, and confirm any external API behavior is acceptable for the workspace. <br>
Risk: The skill encourages high-authority coding-agent workflows that can modify files, run commands, push branches, or post comments. <br>
Mitigation: Use disposable or tightly scoped workdirs, avoid no-approval modes for untrusted tasks, and manually review diffs before commits, pushes, comments, or event commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QCZX0318/coding-agent-backup-fixed-2026q1) <br>
- [Publisher profile](https://clawhub.ai/user/QCZX0318) <br>
- [Gemini API endpoint used by bundled script](https://generativelanguage.googleapis.com/v1/models/gemini-3.1-pro:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime responses may include text and code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PTY-capable bash tool; documented workflows reference Codex, Claude Code, OpenCode, or Pi CLIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
