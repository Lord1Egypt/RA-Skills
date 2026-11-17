## Description:

Launches a browser-based teleprompter with mobile remote control for video recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:

ISC

## Use Case:

External creators and video teams use this skill to run a local browser teleprompter, pair a phone by QR code, and control script page turns while recording video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The LAN-accessible remote-control server allows unauthenticated network clients to read, replace, and control scripts.

Mitigation: Use only on a trusted private network, avoid confidential scripts, stop the server when finished, and prefer a version with pairing tokens, authentication, origin checks, and payload limits.

Risk: The generated QR code exposes the remote-control URL to devices that can reach the same network service.

Mitigation: Display the QR code only in trusted recording environments and rotate or stop the server after the session.

## Reference(s):

- [Clawprompt ClawHub listing](https://clawhub.ai/jiafar/skills/clawprompt)
- [Publisher profile: jiafar](https://clawhub.ai/user/jiafar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and local service URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions to install dependencies, start a local Node.js WebSocket server, and open browser-based teleprompter and remote-control pages.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
