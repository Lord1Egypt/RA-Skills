## Description:

Query Fitbit health data including sleep, heart rate, activity, SpO2, and breathing rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer fitness, sleep, activity, heart-rate, SpO2, breathing-rate, profile, and device-sync questions by running read-only Fitbit CLI queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to read personal Fitbit health, profile, and device data through the local CLI.

Mitigation: Install and authorize fitbit-cli only on trusted machines, review where OAuth tokens are stored, and revoke Fitbit access when it is no longer needed.

Risk: Returned health and activity data may be stale when a Fitbit device has not synced recently.

Mitigation: Check device sync status before relying on recent readings or trend summaries.

## Reference(s):

- [Fitbit](https://www.fitbit.com)
- [ClawHub Fitbit Skill](https://clawhub.ai/mjrussell/skills/fitbit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local fitbit-cli binary and authenticated Fitbit access; Fitbit data may be delayed by device sync.]

## Skill Version(s):

0.1.0 (source: server release metadata, released 2026-01-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
