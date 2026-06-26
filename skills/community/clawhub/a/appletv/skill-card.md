## Description: <br>
Control Apple TV via pyatv for playback, navigation, volume, app launching, power control, discovery, and now-playing status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucaKaufmann](https://clawhub.ai/user/LucaKaufmann) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a paired Apple TV through pyatv commands for media control, navigation, app launch, power, device discovery, and current playback status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a user's Apple TV, including power, navigation, playback, volume, and app launching. <br>
Mitigation: Require confirmation before disruptive actions and limit use to trusted paired devices. <br>
Risk: The appletv.json file stores device identifiers and protocol credentials. <br>
Mitigation: Keep the credential file private, restrict filesystem permissions, and avoid sharing it in logs or support requests. <br>
Risk: The helper depends on pyatv/atvremote installed outside the skill. <br>
Mitigation: Install pyatv from a trusted source and verify the installed version before use. <br>


## Reference(s): <br>
- [ClawHub Apple TV release](https://clawhub.ai/LucaKaufmann/appletv) <br>
- [LucaKaufmann publisher profile](https://clawhub.ai/user/LucaKaufmann) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local pyatv/atvremote commands against a paired Apple TV and read device credentials from appletv.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
