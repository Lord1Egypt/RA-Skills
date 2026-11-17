## Description:

Skill Logger records and queries task history across supported agent platforms, including task parameters, operation steps, results, timestamps, and platform information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist and query task records for Mingri DMP workflows across conversations and supported platforms. It is intended for local auditability and continuity when recording task inputs, steps, statuses, and outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task records can include parameters, results, and operational details that persist across conversations in shared local storage.

Mitigation: Use the skill only for non-sensitive task data, avoid secrets and personal or business-sensitive details, and confine storage to private directories with restrictive permissions when needed.

Risk: Shared history locations can expose task records beyond the current conversation or agent session.

Mitigation: Review storage path behavior before deployment and establish retention, access, and cleanup practices for environments where multiple users or sessions may share local paths.

## Reference(s):

- [ClawHub Skill Logger release page](https://clawhub.ai/mingri26/skills/dmp-skill-logger)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON task records and command-line JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists task history in local JSON files and may reuse records across conversations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
