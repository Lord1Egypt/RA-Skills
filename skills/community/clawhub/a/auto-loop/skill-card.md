## Description: <br>
Auto Loop provides local task scheduling with timed triggers, recurring jobs, status tracking, retries, and failure recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to schedule local recurring or one-time tasks, monitor execution status, and retry or recover failed task runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled task handlers may repeatedly touch files, networks, or services depending on the handler code supplied by the user. <br>
Mitigation: Review each task handler before enabling it, use low retry counts for sensitive actions, and keep a clear stop or unschedule procedure. <br>
Risk: Retries and persisted scheduler state can keep failed or outdated jobs active longer than intended. <br>
Mitigation: Monitor execution history, clear failed tasks when appropriate, and review local JSON state files under auto-loop-state during operation. <br>


## Reference(s): <br>
- [Auto Loop ClawHub release](https://clawhub.ai/pagoda111king/auto-loop) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, YAML, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON state files under auto-loop-state when the scheduler is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
