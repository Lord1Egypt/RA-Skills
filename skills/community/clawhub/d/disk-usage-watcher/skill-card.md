## Description:

Monitors disk space and inode usage on specified paths and sends alerts when configured thresholds are exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidalghetf](https://clawhub.ai/user/nidalghetf)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check disk and inode utilization for selected paths or mounted partitions and receive alerts before disk-full incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect paths, thresholds, alert destinations, or cron cadence can produce noisy alerts or miss disk-full conditions.

Mitigation: Review configured paths, disk and inode thresholds, alert destination, and whether a 15-minute cadence fits the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidalghetf/skills/disk-usage-watcher)

## Skill Output:

**Output Type(s):** [JSON, Text, Notifications]

**Output Format:** [JSON status/details object with disk usage statistics and alert details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run on demand or on a disclosed 15-minute cron cadence.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
