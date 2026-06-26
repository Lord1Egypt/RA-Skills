## Description: <br>
Call Claude Code as a non-interactive coding agent on the same machine as OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxuzzwz](https://clawhub.ai/user/xxuzzwz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to delegate local code exploration, refactoring, bug fixing, batch review, and CI/CD-style checks to Claude Code while an orchestrator coordinates and verifies the work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch Claude Code locally with sensitive Anthropic credentials available to the process. <br>
Mitigation: Install only when local delegation to Claude Code is intended, protect ANTHROPIC_API_KEY and ANTHROPIC_AUTH_TOKEN, and avoid exposing them in logs or shared shells. <br>
Risk: Full-permission non-interactive runs can edit files and run commands without normal approval checkpoints. <br>
Mitigation: Prefer read-only or accept-edits modes; use the permission bypass only in trusted, isolated worktrees after reviewing the command and scope. <br>
Risk: Long-running background Claude Code processes can continue after an orchestration timeout. <br>
Mitigation: Monitor active Claude Code processes before retrying or terminating work, and review command output, git status, diffs, and test results after completion. <br>


## Reference(s): <br>
- [Stream-JSON Processing](references/streaming.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/xxuzzwz/claude-code-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command templates and reference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON or stream-json handling guidance for Claude Code command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
