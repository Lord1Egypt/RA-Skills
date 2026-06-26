## Description: <br>
Async Command guides agents on starting, polling, logging, and stopping long-running shell commands without blocking other work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guytogay](https://clawhub.ai/user/guytogay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to run shell commands asynchronously and how to monitor or stop background jobs during long builds, tests, installs, migrations, or log watches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-running shell commands can keep working in the background after the agent moves on. <br>
Mitigation: Track session IDs, poll or log background jobs periodically, and stop jobs that are no longer needed. <br>
Risk: Shell execution can be destructive or privileged if commands are not scoped to the task. <br>
Mitigation: Keep commands task-scoped, use confirmation for destructive operations, and avoid privileged commands unless explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guytogay/async-command) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell-command patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no hidden install behavior or data access reported by the security evidence.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
