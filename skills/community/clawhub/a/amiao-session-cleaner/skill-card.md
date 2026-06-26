## Description: <br>
Session Cleaner helps OpenClaw users review and clean obsolete session records and related session files while preserving running sessions and main agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macofee](https://clawhub.ai/user/macofee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to inspect session state, identify stale or orphaned session files, and clean them after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup can remove local OpenClaw session history, including transcript, trajectory, and checkpoint files. <br>
Mitigation: Review the proposed agents, sessions, and files before approval, and back up important session data before running cleanup. <br>
Risk: Deleting running sessions or needed history can interrupt active work or remove records the user still needs. <br>
Mitigation: Do not approve deletion of running sessions or history that may be needed later; keep main agent sessions unless there is a clear reason to remove them. <br>


## Reference(s): <br>
- [Session Cleaner on ClawHub](https://clawhub.ai/macofee/amiao-session-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python cleanup code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before deletion and can modify local OpenClaw session files when executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
