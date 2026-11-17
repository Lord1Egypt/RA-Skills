## Description:

Workflow-driven skill that autonomously manages stale items in Google Tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with Google Tasks backlogs use this skill to trigger a backing backlog-grooming workflow that reviews stale tasks and returns a grooming summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backing grooming plugin can automatically change Google Tasks without a clear preview or confirmation step.

Mitigation: Use only with clearly defined grooming rules, limited task-list scope, and a way to preview or recover task changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, API Calls]

**Output Format:** [JSON summary returned by the backing grooming plugin, with agent-facing status or error text when retries fail.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects an empty JSON input object and retries failed or invalid plugin responses up to three times before notifying the user.]

## Skill Version(s):

1.0.2 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
