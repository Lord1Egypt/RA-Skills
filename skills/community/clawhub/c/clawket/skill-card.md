## Description: <br>
Generate QR codes for the Clawket mobile app to pair with the local OpenClaw Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p697](https://clawhub.ai/user/p697) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate a QR code that configures the Clawket mobile app with a local gateway host, port, and auth token for pairing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The QR image and terminal payload contain a live local gateway credential. <br>
Mitigation: Treat the PNG and any copied terminal output like a password, share them only with the intended device, and delete the QR file after pairing. <br>
Risk: The generated QR file is written to disk at ~/.openclaw/media/clawket-qr.png. <br>
Mitigation: Remove the generated file after pairing unless a local retention policy requires keeping it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Text] <br>
**Output Format:** [Markdown guidance with bash command, PNG QR code file, and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires qrencode and an existing OpenClaw gateway configuration at ~/.openclaw/openclaw.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
