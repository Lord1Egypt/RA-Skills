## Description: <br>
Captures snapshots from Ezviz cameras, analyzes them for phone-use behavior, and plays a voice alert on configured devices when phone use is detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to monitor authorized Ezviz camera feeds for phone-use behavior and trigger device audio alerts. It is intended for controlled environments such as classrooms, exam rooms, or meeting rooms where camera monitoring is lawful and disclosed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles surveillance images and can trigger device audio alerts. <br>
Mitigation: Use only with cameras and spaces the operator is authorized to monitor, disclose monitoring as required, and review alert behavior before deployment. <br>
Risk: Ezviz app credentials and device identifiers are required for operation. <br>
Mitigation: Prefer environment variables or a secret manager over command-line credentials, use least-privilege credentials, restrict access where supported, and rotate credentials regularly. <br>
Risk: The security review reports unsafe edges around a remote sound fallback and duplicate alert path. <br>
Mitigation: Remove the remote sound fallback and fix the duplicate alert path before relying on unattended automated alerts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Ezviz-Open/ezviz-open-capture) <br>
- [Ezviz API documentation bundled with the skill](references/ezviz-api-docs.md) <br>
- [Ezviz access token API](https://open.ys7.com/help/81) <br>
- [Ezviz device capture API](https://open.ys7.com/help/687) <br>
- [Ezviz phone detection analysis API](https://open.ys7.com/help/3956) <br>
- [Ezviz voice upload API](https://open.ys7.com/help/1241) <br>
- [Ezviz voice send API](https://open.ys7.com/help/1253) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Console text with setup commands, environment configuration, API status messages, and detection summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a temporary local audio file and send camera snapshots, credentials, device identifiers, and audio files to configured third-party services.] <br>

## Skill Version(s): <br>
1.0.10 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
