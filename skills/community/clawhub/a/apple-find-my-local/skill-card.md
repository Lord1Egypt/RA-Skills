## Description: <br>
Control Apple Find My app via Peekaboo to locate people, devices, and items such as AirTags through local native app automation without third-party APIs or credential sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loganprit](https://clawhub.ai/user/loganprit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to control the native macOS Find My app through local UI automation for locating people, devices, and items, taking screenshots, and attempting supported item actions such as Play Sound. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can view sensitive Find My location data for people, devices, and items. <br>
Mitigation: Use it only when the user expects Find My access, keep the Find My window visible during automation, and avoid sharing screenshots or logs that expose locations or names. <br>
Risk: Screenshots of the Find My window may be written to local storage and can contain sensitive locations and names. <br>
Mitigation: Set FM_OUTPUT_DIR to a private folder when possible and delete Find My screenshots after use. <br>
Risk: Coordinate clicks and Play Sound actions can affect the live macOS session. <br>
Mitigation: Watch automation while it runs, avoid using the Mac concurrently, and confirm actions before running scripts that click coordinates or attempt Play Sound. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loganprit/apple-find-my-local) <br>
- [Publisher profile](https://clawhub.ai/user/loganprit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local screenshot file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Find My.app, OpenClaw.app with Screen Recording and Accessibility permissions, Peekaboo, jq, and a Peekaboo bridge socket.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
