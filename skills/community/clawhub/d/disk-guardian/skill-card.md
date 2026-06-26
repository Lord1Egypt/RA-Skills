## Description: <br>
Run S.M.A.R.T. diagnostics on all drives, parse health indicators, maintain a history log, and flag drives showing early failure patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and system administrators use this skill to check local macOS and Linux drive health, generate S.M.A.R.T. summaries, rank drives by risk, and optionally track health trends over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scan step detects all local physical drives and reads S.M.A.R.T. data from each one. <br>
Mitigation: Run the skill only when local disk-health diagnostics are intended, and review the generated report before acting on replacement or backup recommendations. <br>
Risk: Linux systems may require sudo for smartctl access. <br>
Mitigation: Use sudo only when needed for S.M.A.R.T. access and review commands before execution. <br>
Risk: Recording history can store local hardware identifiers such as drive model and serial number. <br>
Mitigation: Avoid --record on shared machines unless retaining that inventory locally is acceptable, or use --data-dir to control where history is stored. <br>


## Reference(s): <br>
- [SMART Attributes Reference](references/smart-attributes.md) <br>
- [Disk Guardian on ClawHub](https://clawhub.ai/newageinvestments25-byte/disk-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Analysis, Guidance] <br>
**Output Format:** [JSON from scan and parse steps, plus Markdown health reports with risk rankings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write optional local history containing drive model, serial, health metrics, and trend alerts when recording is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
