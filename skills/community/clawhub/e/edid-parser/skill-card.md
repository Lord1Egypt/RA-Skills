## Description:

Parse and analyze EDID (Extended Display Identification Data) from monitors and displays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leyao1017](https://clawhub.ai/user/leyao1017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, test engineers, and display engineers use this skill to inspect EDID data, validate monitor capabilities, troubleshoot display connection issues, and summarize supported modes from Linux sysfs or EDID files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a documented troubleshooting command that writes to a kernel-controlled display sysfs node.

Mitigation: Treat the skill as read-only EDID tooling; use edid-decode on existing EDID files or sysfs reads, and avoid writing to /sys/class/drm paths unless independently confirmed safe for the exact kernel and display driver.

Risk: Parsing results can be incomplete or misleading when EDID data is empty, corrupted, non-standard, or unsupported by edid-decode.

Mitigation: Review validation warnings, confirm critical display capability decisions against hardware documentation, and keep original EDID files for comparison.

## Reference(s):

- [EDID Specification Overview](references/edid_spec.md)
- [EDID Manufacturer Codes](references/manufacturer_codes.md)
- [EDID Parser Skill Feature Plan](references/feature_plan.md)
- [VESA](https://www.vesa.org/)
- [CTA](https://www.cta.tech/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown with command examples, human-readable reports, validation summaries, and structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local EDID files, Linux DRM sysfs availability, and the edid-decode command.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
