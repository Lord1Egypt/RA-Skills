## Description:

Personal device and appliance manager with error code lookup and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udiedrichsen](https://clawhub.ai/user/udiedrichsen)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to track household devices and appliances, store model and warranty details, look up error codes, and get troubleshooting or maintenance guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal device information such as serial numbers, purchase details, warranty dates, and maintenance notes.

Mitigation: Use it only in workspaces where storing this information is acceptable, and avoid entering unnecessary sensitive device details.

Risk: The security summary reports a search-query bug that can expose the handler environment.

Mitigation: Avoid putting secrets in the handler environment until the bug is fixed and the release is rescanned.

Risk: Generated Google search links can include device details and problem descriptions.

Mitigation: Review generated links before opening or sharing them when device information is private.

Risk: Removing a device deletes its record immediately.

Mitigation: Confirm the selected device before removal and keep backups of important records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/udiedrichsen/skills/device-assistant)
- [Publisher profile](https://clawhub.ai/user/udiedrichsen)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands]

**Output Format:** [JSON responses with user-facing troubleshooting, warranty, maintenance, and device-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores device records and history under the workspace memory directory; online lookups are represented as generated search URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
