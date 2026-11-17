## Description:

Find Appian application objects that are missing a description by exporting an application, scanning object XML files, and reporting each object with an empty or absent description tag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarspiker](https://clawhub.ai/user/solarspiker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Appian application administrators use this skill to audit documentation coverage after application changes by listing Appian objects with missing or blank descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards APPIAN_API_KEY to the configured Appian endpoint and packageZip URL.

Mitigation: Use a least-privileged Appian API key and run only against trusted Appian endpoints.

Risk: Exported application ZIPs are saved locally and may remain on disk after the run.

Mitigation: Review and delete files in appian-exports after use when exported application contents are sensitive.

Risk: The scanner notes review-worthy local file overwrite risk around saved ZIP filenames.

Mitigation: Validate packageZip origin and sanitize or inspect saved ZIP filenames before running in sensitive project directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/solarspiker/skills/appian-unnamedobjects)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown-compatible plain text report with object type, name, UUID, and grouped counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY; writes exported application ZIPs to local appian-exports directories.]

## Skill Version(s):

1.3.0 (source: server release metadata and script annotation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
