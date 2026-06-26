## Description: <br>
Execute long-running, multi-session tasks autonomously using Claude Code headless mode or in-session hook-based loops, with structured task decomposition and lightweight iterative modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep Claude Code working across multiple sessions on long-running implementation, testing, bug fixing, refactoring, and batch tasks. It is intended for tasks that benefit from autonomous continuation with progress tracking and explicit completion checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is built for unattended autonomous coding and the security scan says it defaults to permission-bypassed persistent looping. <br>
Mitigation: Install only when autonomous continuation is intentional; prefer disposable or non-production repositories and override the permission mode away from bypassPermissions when possible. <br>
Risk: The headless and hook loops can continue across sessions or iterations until completion criteria or limits are reached. <br>
Mitigation: Set explicit --max-sessions or --max-iterations values, monitor generated logs, and remove .claude/autonomous-loop.local.md to cancel hook-mode loops. <br>
Risk: Autonomous sessions may modify project files without direct review during execution. <br>
Mitigation: Review .autonomous/, .claude/autonomous-loop.local.md, session logs, and all generated code before committing or deploying. <br>


## Reference(s): <br>
- [Autonomous Skill on ClawHub](https://clawhub.ai/feiskyer/autonomous-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated task tracking files, session logs, hook configuration, and code or project file changes produced by the autonomous agent sessions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes progress under .autonomous/ for headless mode and .claude/autonomous-loop.local.md for hook mode; supports structured and lightweight execution strategies.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
