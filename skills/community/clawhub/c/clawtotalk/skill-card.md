## Description: <br>
Set up Claw To Talk, a free push-to-talk mobile voice companion app for OpenClaw on iOS and Android using Tailscale and optional ElevenLabs text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvinunreal](https://clawhub.ai/user/alvinunreal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and OpenClaw developers use this skill to configure mobile push-to-talk voice access from iOS or Android through a Tailscale connection, with optional ElevenLabs voice quality improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OpenClaw gateway is exposed to the user's Tailscale network on port 18789. <br>
Mitigation: Confirm the user is comfortable with this network exposure before setup and keep the gateway bound to the intended Tailscale access path. <br>
Risk: Gateway tokens can grant access if copied into public chats, screenshots, or shared logs. <br>
Mitigation: Generate a strong unique token, store it carefully, avoid public disclosure, and rotate it immediately if exposure is suspected. <br>
Risk: Unintended mobile devices could be approved for voice access. <br>
Mitigation: Approve only the intended device and review the OpenClaw device list during setup. <br>


## Reference(s): <br>
- [Claw To Talk website](https://clawtotalk.com) <br>
- [Claw To Talk setup guide](https://clawtotalk.com/howto) <br>
- [ClawHub skill page](https://clawhub.ai/alvinunreal/clawtotalk) <br>
- [Publisher profile](https://clawhub.ai/user/alvinunreal) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with JSON configuration snippets and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, troubleshooting guidance, and mobile app connection details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
