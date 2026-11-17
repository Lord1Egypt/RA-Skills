## Description:

Checks the status of an Appian deployment by UUID and can optionally poll and download deployment log or package ZIP artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarspiker](https://clawhub.ai/user/solarspiker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill after Appian export or deployment operations to monitor deployment status and retrieve deployment artifacts when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional artifact downloads may send the Appian API key to URLs returned by the deployment API before those URLs are origin-validated.

Mitigation: Use only a trusted Appian base URL with a tightly scoped Appian API key, and avoid --download-log or --download-zip until artifact URL origin validation is added.

Risk: Downloaded artifact filenames may not be safely contained under the advertised export directory.

Mitigation: Avoid download flags until filenames are sanitized and writes are constrained to ~/appian-exports/.

## Reference(s):

- [Appian Deployment Results API](https://docs.appian.com/suite/help/25.4/Get_Deployment_Results_API.html)
- [ClawHub skill page](https://clawhub.ai/solarspiker/skills/appian-deploymtstatus)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text deployment status output with optional downloaded log or ZIP files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY; optional downloads are intended for ~/appian-exports/.]

## Skill Version(s):

1.2.0 (source: server release metadata and script annotation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
