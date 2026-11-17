## Description:

Abby Autonomy helps an agent pull work from a local Markdown task queue, track task state, and continue queued work during scheduled heartbeat checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earnabitmore365](https://clawhub.ai/user/earnabitmore365)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to give an agent a simple autonomous work loop backed by a trusted local task queue and state file. It is suited to recurring low-impact tasks that can be safely paused, reviewed, and completed from queue state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous work can continue without asking each time.

Mitigation: Install only when that behavior is intended, keep the scheduler easy to pause, and limit queued tasks to trusted low-impact work.

Risk: Queue state handling can repeat, lose, or misclaim tasks.

Mitigation: Review queue updates before relying on the skill for important workflows, and avoid financial, account-changing, or costly external actions until queue-claim and parsing issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earnabitmore365/skills/abby-autonomy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helpers and JSON task-state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local queue and status updates; does not provide external service guarantees.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
