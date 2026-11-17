## Description:

Ensures calendar event changes meet attendee, time, privacy, and approval criteria before allowing creation, updates, cancellations, invites, or shares.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and calendar-capable agents use this skill to check attendees, time details, privacy exposure, recurrence, and explicit approval before changing or sharing calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A connected checker may receive redacted meeting-risk summaries that still reveal limited context about planned calendar actions.

Mitigation: Use only a trusted checker and send the minimal redacted review payload rather than full calendars, private notes, links, attendee contact details, or unrelated schedule data.

Risk: Calendar changes can affect other people or expose private information when attendees, timing, recurrence, or approval are unclear.

Mitigation: Require exact attendee, timezone, recurrence, privacy, and approval checks; ask, narrow, request approval, or block when those checks fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-calendar-scheduling-guardrail-skill)
- [Calendar scheduling guardrail schema](artifact/schemas/calendar-scheduling-guardrail.schema.json)
- [Redacted calendar scheduling guardrail example](artifact/examples/redacted-calendar-scheduling-guardrail.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions with a structured text decision summary and optional redacted JSON review payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not execute commands, install dependencies, persist data, call services, or change calendars on its own.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
