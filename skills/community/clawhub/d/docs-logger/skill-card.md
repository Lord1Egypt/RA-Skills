## Description:

Google Docs Log Automation — Append log lines to auto-created daily documents in Google Drive by PortEden Secure Access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to append structured run, audit, task, and error logs to daily Google Docs that are auto-created in Google Drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged content may be stored in Google Drive and could expose secrets, personal data, customer data, or regulated information.

Mitigation: Avoid logging sensitive data unless the storage and retention model has been explicitly approved.

Risk: The PortEden CLI token and connected Google Drive access are cloud-access sensitive.

Mitigation: Verify the PortEden install source, use least-privilege Google access where possible, and restrict sharing on the log folder.

## Reference(s):

- [PortEden](https://porteden.com)
- [ClawHub skill page](https://clawhub.ai/porteden/skills/docs-logger)
- [PortEden ClawHub publisher profile](https://clawhub.ai/user/porteden)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and compact JSON command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the porteden CLI, PE_API_KEY, and a configured PE_LOG_FOLDER for daily Google Docs logging.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
