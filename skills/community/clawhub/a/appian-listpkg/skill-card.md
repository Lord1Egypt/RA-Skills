## Description:

List all packages for an Appian application by UUID. Use when the user wants to see what packages exist in an application, or to find a package UUID before inspecting or deploying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarspiker](https://clawhub.ai/user/solarspiker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Appian administrators use this skill to enumerate packages for a specific Appian application and find package UUIDs before inspecting, exporting, or deploying packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and configuration handling is broader than users should accept without review.

Mitigation: Review before installing, prefer injected environment secrets, and avoid relying on appian.json fallback files.

Risk: An untrusted APPIAN_BASE_URL or parent-directory appian.json file could affect where credentials are used.

Mitigation: Use only trusted APPIAN_BASE_URL values and do not run the skill from directories where an untrusted parent appian.json could be discovered.

## Reference(s):

- [Appian v2 Deployment Management API package management documentation](https://docs.appian.com/suite/help/25.4/Package_Management_API.html)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output listing package names, UUIDs, object counts, timestamps, and optional package metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Appian application UUID and APPIAN_BASE_URL/APPIAN_API_KEY credentials.]

## Skill Version(s):

1.1.0 (source: release metadata and scripts/index.js header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
