## Description: <br>
Broadcasts a local audio file or text-to-speech message to configured Ezviz camera devices using Ezviz Open Platform credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation users use this skill to send voice notifications, reminders, alerts, or prerecorded audio to Ezviz devices that support talk or audio playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Ezviz app credentials to upload audio or generated speech and make configured devices play it. <br>
Mitigation: Use a dedicated least-privilege Ezviz application, verify target device serials and audio content before running, and rotate credentials according to your policy. <br>
Risk: Access tokens are cached by default in a system temporary directory. <br>
Mitigation: Set EZVIZ_TOKEN_CACHE=0 on shared or high-security systems, or clear the cache after use. <br>
Risk: If environment variables are absent, the skill may read Ezviz credentials from OpenClaw configuration files. <br>
Mitigation: Set EZVIZ_APP_KEY, EZVIZ_APP_SECRET, and EZVIZ_DEVICE_SERIAL explicitly so environment variables override local configuration files. <br>
Risk: Audio files, credentials, and device identifiers are sent to the Ezviz Open Platform endpoint to perform the broadcast. <br>
Mitigation: Install and run the skill only when that data flow is intended for the target devices and account. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Ezviz-Open/ezviz-open-camera-broadcast) <br>
- [Ezviz Open Platform](https://open.ys7.com/) <br>
- [Ezviz token API documentation](https://open.ys7.com/help/81) <br>
- [Ezviz voice upload API documentation](https://open.ys7.com/help/1241) <br>
- [Ezviz voice send API documentation](https://open.ys7.com/help/1253) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/status console output from the broadcast script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ezviz app credentials, target device serials, and either an audio file or text content.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
