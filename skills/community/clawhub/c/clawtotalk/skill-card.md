## Description:

Set up Claw To Talk, a free push-to-talk mobile voice companion app for OpenClaw on iOS and Android using Tailscale and optional ElevenLabs text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinunreal](https://clawhub.ai/user/alvinunreal)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill to configure a mobile push-to-talk voice companion with Tailscale connectivity, gateway authentication, device approval, and optional ElevenLabs voice output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup exposes an OpenClaw gateway through Tailscale and requires a gateway token.

Mitigation: Use a unique token for this app, restrict tailnet access where possible, and rotate the token if device access or app trust changes.

Risk: Approving the wrong mobile device could grant unintended access to the OpenClaw gateway.

Mitigation: Verify the exact device ID before approval and revoke devices that are no longer needed.

Risk: Optional ElevenLabs configuration may involve entering a sensitive API key into an external app.

Mitigation: Avoid entering a broad ElevenLabs key unless needed and prefer a key scoped or managed for this app where possible.

Risk: Tailscale Serve may remain active after testing or temporary use.

Mitigation: Know how to turn off Tailscale Serve and disable it when remote voice access is no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvinunreal/skills/clawtotalk)
- [Claw To Talk website](https://clawtotalk.com)
- [Claw To Talk setup guide](https://clawtotalk.com/howto)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup and troubleshooting guidance for OpenClaw gateway, Tailscale, device approval, and optional ElevenLabs configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
