## Description: <br>
Export an Appian application or package to a ZIP file by UUID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarspiker](https://clawhub.ai/user/solarspiker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Appian administrators use this skill to export, download, or back up Appian applications and packages from a configured Appian environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Appian credentials and security evidence notes that credential handling is broader than the user-facing documentation fully controls. <br>
Mitigation: Review before installing, use explicit APPIAN_BASE_URL and APPIAN_API_KEY environment variables, avoid appian.json when possible, and scope credentials to the intended Appian environment. <br>
Risk: The skill downloads and writes ZIP files, and security guidance calls out packageZip host validation and downloaded filename handling as concrete concerns. <br>
Mitigation: Run it from a directory where an appian-exports copy is acceptable, review the resulting ZIP path and filename before use, and prefer a release that validates the packageZip host and sanitizes downloaded filenames. <br>


## Reference(s): <br>
- [Appian v2 Deployment Management Export Package API](https://docs.appian.com/suite/help/25.4/Export_Package_API.html) <br>
- [ClawHub Appian Export release page](https://clawhub.ai/solarspiker/appian-export) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local ZIP file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APPIAN_BASE_URL and APPIAN_API_KEY; writes the exported ZIP to ~/appian-exports/ and may copy it to ./appian-exports/.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
