## Description:

Automates searches for one-way MAO to CNF flights on a twice-daily schedule and reports qualifying results through WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to configure an agent workflow that searches for qualifying one-way flights from Manaus (MAO) to Belo Horizonte/Confins (CNF) and summarizes the five cheapest matches for WhatsApp reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled automation may run before the user has confirmed the intended cron schedule, timezone, and WhatsApp destination.

Mitigation: Review and explicitly approve the cron schedule, America/Manaus timezone, and WhatsApp recipient before enabling automation.

Risk: Flight search and WhatsApp reporting may require credentials or session data outside the bundled skill files.

Mitigation: Keep credentials out of skill files and reports, use the minimum required access, and verify secret handling before running the workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with configuration guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports up to the five cheapest matching one-way flight options based on the configured route, date, duration, connection, arrival-time, carrier-priority, and price criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
