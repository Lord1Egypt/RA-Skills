## Description:

Export an Appian application or package to a ZIP file by UUID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarspiker](https://clawhub.ai/user/solarspiker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Appian administrators use this skill to export, download, or back up Appian applications or packages from a configured Appian environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Appian API key may be sent to an unvalidated ZIP download URL.

Mitigation: Use only trusted Appian environments and validate the ZIP download URL against the configured Appian origin before normal use.

Risk: ZIP filenames may write outside the intended export folder.

Mitigation: Avoid attacker-controlled export names and sanitize or generate local filenames before treating the skill as safe for normal use.

## Reference(s):

- [Appian Export Package API documentation](https://docs.appian.com/suite/help/25.4/Export_Package_API.html)
- [Appian Export skill page](https://clawhub.ai/solarspiker/skills/appian-export)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and local ZIP file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY; saves exported ZIP files locally.]

## Skill Version(s):

1.3.0 (source: server release metadata and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
