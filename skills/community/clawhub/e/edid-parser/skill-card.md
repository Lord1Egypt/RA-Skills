## Description: <br>
Parse and analyze EDID (Extended Display Identification Data) from monitors and displays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leyao1017](https://clawhub.ai/user/leyao1017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, test engineers, and display troubleshooting teams use this skill to inspect monitor EDID data, validate display capabilities, diagnose HDMI, DRM, and KMS issues, and batch-check EDID files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes display troubleshooting guidance around Linux sysfs EDID paths, and server security evidence warns against commands that write to /sys/class/drm unless the operator understands the system impact. <br>
Mitigation: Use the included parsing and validation scripts for read-only EDID inspection, and avoid sysfs write commands or elevated privileges unless intentionally performing advanced display troubleshooting. <br>


## Reference(s): <br>
- [EDID Specification Overview](references/edid_spec.md) <br>
- [EDID Manufacturer Codes](references/manufacturer_codes.md) <br>
- [EDID Parser Feature Plan](references/feature_plan.md) <br>
- [VESA](https://www.vesa.org/) <br>
- [CTA](https://www.cta.tech/) <br>
- [ClawHub Skill Page](https://clawhub.ai/leyao1017/edid-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable reports, JSON data, validation results, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against EDID binary files, raw hex data, or Linux sysfs EDID paths; requires edid-decode for full parsing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
