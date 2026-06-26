## Description: <br>
Ensures calendar event changes meet attendee, time, privacy, and approval criteria before allowing creation, updates, cancellations, invites, or shares. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this instruction-only skill to make an OpenClaw-style agent verify attendee, time, recurrence, privacy, and explicit approval details before changing calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar changes can affect other people or expose private meeting details when attendees, time, recurrence, or visibility are unclear. <br>
Mitigation: Verify exact attendees, timezone, date, duration, recurrence, private notes, guest visibility, and explicit approval before proceeding. <br>
Risk: External guests, broad group aliases, recurring edits, cancellations, or high-impact meetings can create wider-than-intended notifications or disclosures. <br>
Mitigation: Ask for clarification, narrow the change, or request approval before inviting external guests, changing recurring events, notifying attendees, or using broad groups. <br>
Risk: Review payloads may include unnecessary calendar data, meeting links, private notes, or attendee contact details. <br>
Mitigation: Use only a minimal redacted review payload when a checker is configured, and omit full calendars, private notes, meeting links, contact details, and unrelated schedule data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-calendar-scheduling-guardrail-skill) <br>
- [README](artifact/README.md) <br>
- [Calendar scheduling guardrail schema](artifact/schemas/calendar-scheduling-guardrail.schema.json) <br>
- [Redacted calendar scheduling guardrail example](artifact/examples/redacted-calendar-scheduling-guardrail.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Configuration] <br>
**Output Format:** [Markdown instructions with a structured text decision pattern and optional redacted JSON review payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute commands, write files, call calendar services, persist memory, or schedule events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
