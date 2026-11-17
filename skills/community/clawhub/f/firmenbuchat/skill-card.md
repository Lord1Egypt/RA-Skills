## Description:

CLI fuer den Zugriff auf das oesterreichische Firmenbuch (HVD WebServices).

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasogott](https://clawhub.ai/user/pasogott)

### License/Terms of Use:


## Use Case:

External users and developers use this skill as a command reference for configuring and operating the firmenbuchat CLI to query Austrian company register records, documents, and change feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI requires a Firmenbuch API key, which could be exposed through committed files, logs, or shared shell history.

Mitigation: Keep the API key out of committed files, logs, and shared shell history; use reviewed local configuration or environment handling.

Risk: Large document-change requests may fail with server-side 5xx responses.

Mitigation: Use smaller time windows for change queries and retry with narrower date ranges.

Risk: Installation uses third-party package sources that are outside NVIDIA ownership.

Mitigation: Review the referenced package source or tap and prefer a pinned or reviewed version before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pasogott/skills/firmenbuchat)
- [Publisher profile](https://clawhub.ai/user/pasogott)
- [Project homepage](https://github.com/pasogott/firmenbuch-aip)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, command usage, output option, pagination, and troubleshooting guidance for the firmenbuchat CLI.]

## Skill Version(s):

0.2.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
