## Description:

Generate QR codes for the Clawket mobile app to pair with the local OpenClaw Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p697](https://clawhub.ai/user/p697)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw Gateway users use this skill to generate a QR code that lets the Clawket mobile app configure a local Gateway connection with host, port, token, and TLS settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated PNG and terminal QR include a live OpenClaw Gateway auth token and should be treated like a password.

Mitigation: Avoid shared or logged terminals, share the QR only with the intended device, delete ~/.openclaw/media/clawket-qr.png after pairing, and rotate the Gateway token if the QR payload is exposed.

Risk: Release security evidence reports a script injection flaw that should be reviewed before installation.

Mitigation: Review the script before use and fix it to pass configuration values to Python as data rather than source code.

## Reference(s):

- [Clawket Skill Page](https://clawhub.ai/p697/skills/clawket)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated QR image output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates ~/.openclaw/media/clawket-qr.png and may print an ASCII QR code containing the Gateway token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
