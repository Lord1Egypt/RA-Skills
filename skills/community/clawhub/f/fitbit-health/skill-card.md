## Description:

Query Fitbit health data (activity, sleep, heart rate, weight) via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pb3975](https://clawhub.ai/user/pb3975)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to let an agent retrieve Fitbit profile, activity, sleep, heart-rate, and weight data through the Fitbit CLI after OAuth authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Fitbit health and profile data after OAuth authorization.

Mitigation: Install it only when that access is intended, review the Fitbit consent screen, and avoid sharing verbose or JSON outputs that may expose personal health data.

Risk: OAuth tokens are stored locally and could be exposed on shared or higher-risk systems.

Mitigation: Use the skill on a single-user trusted machine where token files are protected, and harden token storage before multi-user deployment.

Risk: Dependency or OAuth scope weaknesses can increase exposure for normal agent use.

Mitigation: Pin and review dependencies and keep OAuth permissions limited to the Fitbit data needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pb3975/skills/fitbit-health)
- [ClawHub publisher profile](https://clawhub.ai/user/pb3975)
- [Fitbit developer app registration](https://dev.fitbit.com/apps)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text or JSON output with setup and authentication commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the fitbit CLI binary and a user-authorized Fitbit OAuth session.]

## Skill Version(s):

0.1.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
