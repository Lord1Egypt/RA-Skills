## Description: <br>
Professional utility to refine terminal-based ASCII and Unicode QR code blocks into high-definition PNG images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdchi](https://clawhub.ai/user/jdchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert terminal-rendered QR code blocks into scannable PNG images when terminal alignment or font rendering makes the original QR code unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR codes can contain short-lived login or account-linking data that should be treated as sensitive. <br>
Mitigation: Use the skill only on QR content the user intends to scan, keep temporary QR text in a private location, and delete temporary text and generated image files when no longer needed. <br>
Risk: A generated QR image may be scanned without verifying what flow it represents. <br>
Mitigation: Confirm the QR code source and expected destination before scanning or sharing the rendered PNG. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jdchi/cli-qr-refiner) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files with concise Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on a text input path, PNG output path, and optional scale value.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
