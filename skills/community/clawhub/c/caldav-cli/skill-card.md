## Description:

Manage CalDAV calendars (iCloud, Google, Yandex) from the command line. Supports OAuth2 and Basic auth, multi-account, table/JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberash-dev](https://clawhub.ai/user/cyberash-dev)

### License/Terms of Use:


## Use Case:

Developers and command-line users use this skill to install and operate caldav-cli for account setup, event listing, and event creation across CalDAV calendar providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The global npm install is unpinned and the installed CLI can access calendar account data.

Mitigation: Review or pin the caldav-cli package before installation and grant only the minimum calendar and account access required.

Risk: Account setup requires calendar credentials or OAuth secrets.

Mitigation: Use the documented OS keychain storage path for secrets, keep account metadata permissions restricted, and revoke credentials when access is no longer needed.

## Reference(s):

- [Caldav Cli on ClawHub](https://clawhub.ai/cyberash-dev/skills/caldav-cli)
- [caldav-cli source](https://github.com/cyberash-dev/caldav-cli)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, JSON]

**Output Format:** [Markdown with inline bash code blocks and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes interactive and non-interactive command examples for account and event workflows.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
