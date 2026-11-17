## Description:

Track tasks and deadlines, update completion status, and identify approaching or overdue work using a local persistent task store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snehanshu-raj](https://clawhub.ai/user/snehanshu-raj)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to record tasks, update their status, and review upcoming or overdue work from a local task store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had incomplete code coverage, so some host-access behavior was not fully assessed.

Mitigation: Review the bundled code and confirm its local file access and task storage path fit your environment.

Risk: The task store's SQLite lock file is not suitable for Cloud Storage FUSE.

Mitigation: Keep the state file on local storage, as the skill documentation advises.

## Reference(s):

- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [SQLite transaction documentation](https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions)
- [Deadline Sentinel on ClawHub](https://clawhub.ai/snehanshu-raj/skills/deadline-sentinel)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON task, status, and alert results from a Node.js CLI, with Markdown usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts identify due and overdue task candidates; they do not schedule notifications.]

## Skill Version(s):

1.0.0 (source: release metadata, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
