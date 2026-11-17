## Description:

Audits embedded OTA and bootloader code for common upgrade failures and provides tools to plan partitions, calculate checksums, package firmware, and verify upgrade packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

Embedded developers use the skill to review IAP and OTA upgrade code, investigate firmware upgrade failures, and prepare firmware packages and partition layouts. It provides findings with repair guidance and helps check packages before device testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review gave a suspicious verdict and was incomplete; it reported a potentially unsafe partition-header generator and a report-page script injection weakness.

Mitigation: Consider avoiding installation until the partition-header issue and incomplete analysis are resolved. If used, handle generated HTML reports cautiously and review outputs from overflowing layouts.

## Reference(s):

- [OTA pre-flight checklist](references/ota-checklist.md)
- [Changelog](references/CHANGELOG.md)
- [ClawHub skill page](https://clawhub.ai/liujycode/skills/embedded-ota-toolkit)

## Skill Output:

**Output Type(s):** [Analysis, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Audit findings and repair guidance, JSON or HTML reports, generated C headers, and firmware package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include static audit findings, package verification results, partition layout configuration, and generated firmware package files.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
