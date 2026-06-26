## Description: <br>
Generate QR codes from text or URLs for easy sharing and scanning. Outputs as ASCII art or image files for printing and digital use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other external users use this skill to create QR codes from text, URLs, or contact information for scanning, sharing, printing, or terminal display. When the optional reader dependencies are available, it can also decode QR codes from local image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Caller-selected input and output file paths can read the wrong local image or overwrite an unintended file. <br>
Mitigation: Choose paths deliberately, prefer a dedicated working directory, and review the target output path before writing. <br>
Risk: QR generation and reading depend on local Python packages such as qrcode, Pillow, and pyzbar. <br>
Mitigation: Use a trusted Python environment and install dependencies from trusted package sources before running the tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/dinghaibin-qrcode-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Terminal text, ASCII QR output, or PNG image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output file path and QR size are caller-selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
