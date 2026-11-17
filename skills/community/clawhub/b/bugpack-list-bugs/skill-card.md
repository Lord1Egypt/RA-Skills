## Description:

Lists tracked bugs from a local BugPack server with optional project filtering and status grouping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duhuazhu](https://clawhub.ai/user/duhuazhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to ask an agent for the current BugPack backlog, optionally filter by project, and receive a status-grouped table for triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad requests about bugs or pending issues even when the user is not asking about BugPack.

Mitigation: Confirm BugPack is the intended issue source or use narrower trigger wording in deployments that track issues elsewhere.

Risk: The skill depends on a local BugPack server being available and returning current bug data.

Mitigation: Verify the local BugPack service is running before relying on the listed bugs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duhuazhu/skills/bugpack-list-bugs)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown table grouped by bug status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bug id, title, status, priority, project_id, created_at, and updated_at when returned by BugPack.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
