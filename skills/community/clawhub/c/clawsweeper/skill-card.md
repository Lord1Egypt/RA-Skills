## Description:

Inspect ClawSweeper issue/PR reports, queue health, and Actions runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Repository maintainers and developers use ClawSweeper to inspect issue and pull request reports, monitor GitHub Actions and repair queues, and request guarded repair workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan could not match three referenced local paths, so those paths were not fully covered.

Mitigation: Inspect the three referenced paths manually before relying on related commands or guidance.

Risk: Repair and automerge workflows can change GitHub state when their execution gates are open.

Mitigation: Use them only for authorized maintainer requests and confirm current-head review, green checks, mergeability, human-review labels, draft status, and required merge gates.

## Reference(s):

- [ClawSweeper on ClawHub](https://clawhub.ai/hillstreet-ph/skills/clawsweeper)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command examples and report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide read-only findings or steps for explicitly authorized repair workflows.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
