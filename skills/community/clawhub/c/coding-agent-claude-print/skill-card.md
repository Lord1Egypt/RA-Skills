## Description: <br>
Delegate coding tasks to Codex, Claude Code, or Pi agents via background process, with guidance for PTY use, Claude Code print mode, PR review, refactoring, and iterative code work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate coding, refactoring, PR review, and multi-worktree tasks to Codex, Claude Code, OpenCode, or Pi agents while choosing the correct execution mode for each tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages delegated coding agents with broad autonomy, including permission bypass and no-sandbox modes. <br>
Mitigation: Use sandboxed or approval-based execution when possible, and avoid permission bypass modes in repositories containing secrets or deployment credentials. <br>
Risk: Background agent sessions can make file changes or prepare remote publishing steps that are easy to miss. <br>
Mitigation: Monitor session logs, review all diffs before committing or pushing, and run PR reviews in temporary clones or isolated worktrees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielsinewe/coding-agent-claude-print) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one of the claude, codex, opencode, or pi CLIs when the guidance is executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
