## Description:

Installs, runs, recovers, or explains the standalone ClawPatch queue supervisor for repair queues, exact stopped-finding recovery, and completion proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to supervise ClawPatch repair queues for repositories they control, including normal runs, exact stopped-checkpoint recovery, and completion proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the supervisor with the wrong repository, branch, push policy, or reset mode can change repository state unexpectedly.

Mitigation: Confirm the repository path, branch, push policy, and reset or resume mode before running the supervisor.

Risk: Ambiguous stopped-checkpoint recovery can mix unrelated source changes with a repair attempt.

Mitigation: Resume only from an exact stopped checkpoint and fail closed when ownership, paths, or repair state are ambiguous.

## Reference(s):

- [ClawPatch Supervise project and install instructions](https://github.com/uncmatteth/clawpatch-supervise)
- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/clawpatch-supervise)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes repository path, branch, supervisor and ClawPatch versions, run mode, current finding or COMPLETE result, stopped paths or proof path, and Git state.]

## Skill Version(s):

0.1.16 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
