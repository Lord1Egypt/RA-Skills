## Description: <br>
Controls a Bambu P1S 3D printer over FTPS for file listing, upload, download, deletion, size checks, and basic connectivity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayf3](https://clawhub.ai/user/mayf3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and printer operators use this skill to manage files on a configured Bambu P1S printer, including listing printer storage, uploading print files, downloading timelapse media, checking file sizes, and checking basic connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release publicly includes a real printer access code and device identifiers. <br>
Mitigation: Rotate the printer access code before use, remove real IP, serial, and access-code values from the package, and keep credentials in a private local configuration outside the skill. <br>
Risk: The skill can delete files from the printer without clear safeguards. <br>
Mitigation: Add explicit user confirmation and path validation before any delete operation, and review each command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mayf3/bambu-printer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mayf3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command output as text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May list, upload, download, size-check, or delete files on a configured printer; security evidence marks this release suspicious and recommends review before installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
