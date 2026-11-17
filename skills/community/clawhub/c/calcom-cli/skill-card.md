## Description:

Manage Cal.com calendars through a CLI for schedules, bookings, event types, available slots, and user profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage Cal.com scheduling workflows from an agent session, including calendar availability, bookings, event types, slot queries, and profile inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses mutable third-party installation commands and may link a CLI into the user's PATH.

Mitigation: Review installation commands before running them and prefer trusted, pinned, verified dependency sources.

Risk: The skill stores a Cal.com API token in a local file.

Mitigation: Use the least-privileged token available, protect local file permissions, and remove the token when it is no longer needed.

Risk: The skill enables account-changing calendar actions such as create, update, delete, cancel, confirm, and reschedule.

Mitigation: Require explicit user confirmation before mutating Cal.com schedules, bookings, or event types.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/melvynx/skills/calcom-cli)
- [Bun install script referenced by setup](https://bun.sh/install)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and standardized JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-driven CLI calls should use --json; mutating calendar actions can create, update, delete, cancel, confirm, or reschedule Cal.com resources.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
