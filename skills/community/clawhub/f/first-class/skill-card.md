## Description:

Helps agents find first class and premium cabin travel options by querying flyai for live flight availability, prices, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to collect first class flight search parameters, run live flyai searches, and present bookable premium cabin options with real-time prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install and run an unpinned global flyai CLI, including a sudo fallback in artifact guidance.

Mitigation: Use a pinned, non-root, sandboxed CLI installation and do not allow automatic global or sudo npm installation.

Risk: Raw travel queries and command execution logs may expose itinerary or booking intent.

Mitigation: Avoid storing raw execution logs; if logging is required, minimize, redact, and give users clear control over retention.

Risk: Booking links or provider identity could be misunderstood before a user acts on travel results.

Mitigation: Confirm provider identity and booking-link domains before presenting or acting on results.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [First Class Flight Playbooks](references/playbooks.md)
- [Fallback Handling](references/fallbacks.md)
- [Execution Log Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking-link tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Every shown travel result must include a booking link from live flyai output.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
