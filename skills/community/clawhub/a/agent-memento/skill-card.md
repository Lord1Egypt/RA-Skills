## Description: <br>
Agent Memento scaffolds tick-driven autonomous coding projects that use Markdown plans, recurring workers, verification commands, git checkpoints, and an optional dashboard to coordinate long-running LLM work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangwenyu2](https://clawhub.ai/user/yangwenyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up a local autonomous coding workflow where a main planning agent breaks work into Markdown tickets and recurring worker agents execute, verify, report, and checkpoint each task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring worker agents can run shell commands and modify project files based on MASTER_PLAN.md verify steps. <br>
Mitigation: Install and run the skill only in a disposable sandbox, VM, container, or dedicated git worktree, and review every verify command before enabling automatic execution. <br>
Risk: Rollback and cleanup behavior can affect tracked and untracked files in the initialized project directory. <br>
Mitigation: Do not initialize Agent Memento in a repository with valuable uncommitted work, secrets, private notes, or production credentials. <br>
Risk: The optional dashboard preview can expose files from the project directory when preview hosting is enabled. <br>
Mitigation: Keep dashboard preview disabled unless the project directory contains no sensitive files, and avoid public host binding. <br>


## Reference(s): <br>
- [Agent Memento on ClawHub](https://clawhub.ai/yangwenyu2/agent-memento) <br>
- [Publisher profile](https://clawhub.ai/user/yangwenyu2) <br>
- [Artifact README](README.md) <br>
- [Complete Skill Specification](SKILL.md) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown plans and status logs, shell commands, generated project files, dashboard configuration, and code changes from worker agents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local project scaffolding, MASTER_PLAN.md, PROJECT_MAP.md, TICK_STATUS.md, HUMAN_NOTES.md, cron-ready worker scripts, git commits, and optional dashboard output.] <br>

## Skill Version(s): <br>
2.0.15 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
