## Description: <br>
Generates QR code images from text, URLs, or WiFi details with configurable size, color, and save path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amzulin](https://clawhub.ai/user/amzulin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to turn text, URLs, phone numbers, or WiFi configuration strings into QR code image files and receive the saved path or an actionable error. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run pip automatically to install qrcode and Pillow when loaded. <br>
Mitigation: Review dependencies first and install them yourself in an isolated virtual environment before enabling the skill. <br>
Risk: Generated QR images are written to disk and may contain sensitive text, URLs, or WiFi information. <br>
Mitigation: Choose an explicit save path with appropriate access controls and avoid storing sensitive QR codes in shared locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amzulin/generate-qr-code-amzulin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Guidance] <br>
**Output Format:** [Text response with a generated QR code image file path or an error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a QR code image to the requested path or the desktop by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
