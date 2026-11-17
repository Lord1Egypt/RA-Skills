## Description:

Query eBusy-based tennis hall bookings via a small Python client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogruenig](https://clawhub.ai/user/ogruenig)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query configured eBusy tennis hall reservation data for a selected court module, date, and optional time window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs an eBusy username and password and may send credentials to any configured EBUSY_BASE_URL.

Mitigation: Use only runtimes that validate EBUSY_BASE_URL against real https://*.ebusy.de hosts before login and prefer a dedicated low-privilege eBusy account.

Risk: The permissions manifest includes filesystem read access that is not necessary for normal reservation lookup.

Mitigation: Remove unnecessary filesystem read permission or restrict it to the skill files required by the runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ogruenig/skills/ebusy-courts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance and shell commands; the bundled Python client prints JSON reservation and availability data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment-provided eBusy base URL, username, password, court module ID, and optional first court number.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
