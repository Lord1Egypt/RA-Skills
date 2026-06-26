## Description: <br>
Generates QR-code image files from text, URLs, or WiFi details with configurable size, color, and save path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YangZhenFu](https://clawhub.ai/user/YangZhenFu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when a user needs a QR code for plain text, a URL, or WiFi connection details and wants the generated image saved to a chosen local path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loading the skill can automatically run unpinned pip installs and alter the Python environment without clear user approval. <br>
Mitigation: Review before installing and prefer declaring qrcode and Pillow as install-time dependencies rather than installing them automatically. <br>
Risk: QR codes may contain passwords, private URLs, or personal data, and generated files can be written to shared or synced folders. <br>
Mitigation: Avoid sensitive QR payloads in shared locations and specify a safe output path to reduce accidental disclosure or overwrites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YangZhenFu/generate-qr-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [PNG image file plus a text status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves qr_code.png to a user-specified path or to the Desktop by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
