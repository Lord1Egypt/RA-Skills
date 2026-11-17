## Description:

Schedule, inspect, retry, pause, resume, stop, and decommission unattended Codex CLI jobs through macOS launchd, Linux systemd user timers, or Windows Task Scheduler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to schedule unattended Codex CLI work, inspect run evidence, and manage recurring or delayed jobs through the host operating system's native scheduler.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended jobs can run Codex later or repeatedly with the configured working directory, prompt, environment, and permissions.

Mitigation: Review each job's cwd, prompt, schedule, write permissions, captured environment variables, and retention settings before creating or updating it.

Risk: Native scheduler persistence may continue launching jobs after the immediate task is complete.

Mitigation: Use pause, decommission, or purge when scheduled execution or stored run artifacts are no longer wanted.

## Reference(s):

- [Operational semantics](references/semantics.md)
- [ClawHub skill page](https://clawhub.ai/wufei-png/skills/codex-native-scheduler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, inspect, update, pause, resume, retry, stop, decommission, or purge native scheduler job state when the user invokes the bundled CLI.]

## Skill Version(s):

0.1.0 (source: release evidence and package __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
