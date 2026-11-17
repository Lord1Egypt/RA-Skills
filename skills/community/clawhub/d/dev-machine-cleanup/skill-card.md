## Description:

Asynchronously cleans old logs and temporary files on the datax development machine while reporting progress and completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to delegate cleanup of development-machine logs, temporary files, and optional Docker artifacts while continuing other work. It is intended for controlled maintenance of the datax development machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asynchronous cleanup can delete remote development-machine files without an explicit review step.

Mitigation: Require explicit confirmation before execution and make the first run a dry run or list-only report.

Risk: Broad cleanup paths can remove files outside the intended maintenance scope.

Mitigation: Restrict cleanup to known log and temporary directories under approved paths, and keep audit logs or backups.

Risk: Docker pruning can remove artifacts needed by other workloads on the machine.

Mitigation: Avoid daemon-wide Docker pruning unless separately approved for that host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexmayanjun-collab/skills/dev-machine-cleanup)
- [Publisher profile](https://clawhub.ai/user/alexmayanjun-collab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown status updates with inline shell commands and cleanup summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include disk-usage before and after cleanup, deleted-file counts, freed-space estimates, and error notifications.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
