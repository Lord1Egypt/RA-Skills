## Description: <br>
Use when an AI coding agent needs bounded development loops, persistent project-local Docs/ state, context budgeting, environment escalation rules, safe stop gates, and Done / Done with Risk / Blocked completion decisions across Codex, Claude Code, OpenCode, Cline, Qoder, CodeBuddy, Trae, Gemini CLI, Aider, GitHub Actions, or other AI coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[englandtong](https://clawhub.ai/user/englandtong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run AI coding work as bounded loops with durable project-local state, verification evidence, stop gates, and handoff-ready status. It is suited for coding tasks that need repeatable progress tracking across agents, runners, or sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PowerShell runner can execute a user-provided local command as part of an automated loop. <br>
Mitigation: Pass only a command you chose and trust, and require explicit per-run approval before destructive operations or privileged work enter an automatic loop. <br>
Risk: Project-local Docs/ state and runner logs may capture sensitive context if the skill is used around secrets, account sessions, production data, or private artifacts. <br>
Mitigation: Keep secrets, production data, account sessions, and sensitive files outside Docs/ and logs; record only the needed credential or access class when human input is required. <br>
Risk: Automated coding loops can continue after partial failures unless stop gates and verification evidence are respected. <br>
Mitigation: Use the skill's stop states and checker evidence before marking work Done, and stop for human approval when security, environment, destructive-change, or account-access gates are triggered. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/englandtong/agent-loop-engineering) <br>
- [Agent Loop Engineering skill definition](SKILL.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Loop State Protocol](references/loop-state-protocol.md) <br>
- [Checker And Evidence Gate](references/checker-and-evidence.md) <br>
- [Automation Runner](references/automation-runner.md) <br>
- [Runner Adapters](references/runner-adapters.md) <br>
- [Completion Gate](references/completion-gate.md) <br>
- [Environment Escalation](references/environment-escalation.md) <br>
- [Host Runtime Integration And Feedback Governance](references/host-runtime-integration.md) <br>
- [AI Coding Production System](references/ai-coding-production-system.md) <br>
- [Harness Engineering](references/harness-engineering.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, project-state templates, JSONL evidence records, and PowerShell or Node.js checker and runner scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local Docs/ state, loop reports, verification evidence, and optional runner or checker commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
