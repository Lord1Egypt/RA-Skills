## Description:

Helps prepare HTML deliverables with an embedded SHA-256 content fingerprint, a timestamp, and a separate checksum file for integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code only); documentation and theory all rights reserved

## Use Case:

Authors and teams preparing HTML reports or other HTML deliverables use this skill to embed a content fingerprint and timestamp and generate a checksum file for later integrity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the helper changes the selected HTML file and creates a checksum file.

Mitigation: Use it only on intended files and review the results before publishing.

Risk: The default timestamp uses GMT+8, which may not match the intended time zone.

Mitigation: Pass a custom stamp when a different time zone or timestamp is required.

## Reference(s):

- [Fingerprint Delivery on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/fingerprint-delivery)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and shell commands; edited HTML and a .sha256 file when run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to the selected HTML file and creates a separate checksum file.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; bundled manifest and skill frontmatter say 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
