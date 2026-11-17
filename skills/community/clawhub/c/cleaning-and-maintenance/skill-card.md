## Description:

Schedule cleanings, manage maintenance tasks, check availability, and add service professionals with TIDY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mchusma](https://clawhub.ai/user/mchusma)

### License/Terms of Use:

MIT-0

## Use Case:

Property managers, Airbnb hosts, and cleaning service coordinators use this skill to operate TIDY API workflows for cleaning bookings, maintenance tasks, service professionals, availability checks, and to-do lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a TIDY account token that may not expire.

Mitigation: Install only if agent access to the TIDY token is acceptable, and keep the token in the required TIDY_API_TOKEN environment variable rather than sharing it in prompts or logs.

Risk: The skill can cancel bookings, reschedule bookings, delete maintenance tasks, and process natural-language multi-step requests.

Mitigation: Require the agent to show exact booking or task details and wait for explicit approval before cancellation, reschedule, deletion, or multi-step requests.

Risk: The artifact mentions an optional global CLI install path.

Mitigation: Prefer the direct API examples unless the CLI package source and version have been independently verified.

## Reference(s):

- [TIDY](https://tidy.com)
- [ClawHub skill page](https://clawhub.ai/mchusma/skills/cleaning-and-maintenance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TIDY_API_TOKEN for authenticated TIDY API requests.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
