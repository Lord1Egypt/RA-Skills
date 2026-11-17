## Description:

Helps agents manage Acuity Scheduling appointments, calendars, clients, and availability through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams managing appointments use this skill to check availability, schedule or change bookings, and manage clients and calendars. It can also guide user-approved automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Maton grants access to the authorized Acuity Scheduling account.

Mitigation: Approve the OAuth connection deliberately and connect only the account needed for the task.

Risk: Creating, changing, or deleting appointments and client records can affect schedules and personal data.

Mitigation: Check the target and intended change, then obtain explicit approval before each write.

Risk: Hosted functions, triggers, or destinations can keep running or forwarding data after the immediate task.

Mitigation: Review their behavior and destination URLs before approval, and remove automations when no longer needed.

## Reference(s):

- [Acuity Scheduling skill release](https://clawhub.ai/byungkyu/skills/acuity-scheduling)
- [Publisher profile](https://clawhub.ai/user/byungkyu)
- [Acuity Scheduling API Quick Start](https://developers.acuityscheduling.com/reference/quick-start)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include appointment or client information returned by an authorized connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
