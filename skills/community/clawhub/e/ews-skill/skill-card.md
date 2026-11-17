## Description:

Extract calendar events from Microsoft Exchange via EWS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[basuev](https://clawhub.ai/user/basuev)

### License/Terms of Use:

MIT

## Use Case:

Employees and developers use this skill to retrieve Microsoft Exchange calendar events for today, tomorrow, or a specific date as structured JSON for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Exchange credentials and sensitive meeting data.

Mitigation: Use OS keyring setup with interactive password entry, protect the local machine, and avoid plaintext .env files or command-line password arguments.

Risk: A misconfigured or untrusted Exchange endpoint could expose credentials or calendar contents.

Mitigation: Configure only trusted HTTPS EWS endpoints and review the EWS_URL before installation or execution.

Risk: Debug XML and output files can contain sensitive meeting details.

Mitigation: Write debug XML and calendar output only to private directories, and delete those files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/basuev/skills/ews-skill)
- [Publisher profile](https://clawhub.ai/user/basuev)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, files, configuration]

**Output Format:** [JSON array of calendar event objects, returned on stdout or written to an output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Events include subject, start and end times, location, organizer, body text, and extracted links; no events are returned as an empty array.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
