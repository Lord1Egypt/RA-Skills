## Description:

Restore a gateway to its last known-good configuration, or tag the current config as known-good when a gateway config change needs a fast rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfdeadcat](https://clawhub.ai/user/halfdeadcat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to restore Slack or Discord gateway configuration from a known-good backup, tag the current configuration as known-good, and restart the gateway with health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live Slack or Discord gateway configuration changes and restart services.

Mitigation: Install and invoke it only on gateway hosts where the operator expects those live changes and restarts.

Risk: Broad natural-language triggers can execute restore behavior without clear confirmation or operator control.

Mitigation: Add an explicit confirmation step before restore or tag actions, especially in production environments.

Risk: Detached execution and temporary logging can make status and auditability harder to monitor.

Mitigation: Prefer a non-detached execution path with visible status output and a secure temporary log path.

Risk: Rollback handling may require correction before production use.

Mitigation: Review and test rollback behavior on a non-critical gateway before installing on an active host.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and operational status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate gateway configuration file changes and service restarts when executed in an appropriate host environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
