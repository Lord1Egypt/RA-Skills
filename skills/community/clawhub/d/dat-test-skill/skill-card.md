## Description:

ByteRover usage metrics report that runs the metrics script to summarize query and curate activity, including counts, durations, file changes, and quota errors across one or more project directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datpham-6996](https://clawhub.ai/user/datpham-6996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run ByteRover health and usage checks for one or more project directories. It summarizes query activity, curate activity, file changes, and quota or rate-limit issues for routine reporting or scheduled checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime instructions and script behavior can execute unpinned or unintended shell code in some environments.

Mitigation: Review before installing or running, especially in CI or cron, and prefer a pinned local dependency instead of unversioned npx.

Risk: BRV_CMD and BRV_SINCE can change command execution or query scope if populated from untrusted sources.

Mitigation: Use trusted configuration values only until the script validates inputs and uses argument-array execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with metric sections and a status line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report one or more project directories; output highlights query activity, curate activity, quota warnings, and overall health.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
