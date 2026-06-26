## Description: <br>
Search and play Netflix content on Android TV. When the user asks to play a specific Netflix title on TV, the agent looks up the title ID and executes ADB commands for precise playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiayun](https://clawhub.ai/user/jiayun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to control an authorized Android TV from an agent session and open a specific Netflix title by ID. It is useful when the user wants direct playback and basic Android TV media controls through ADB. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ADB debugging grants remote control over the Android TV when a computer is authorized. <br>
Mitigation: Use only a trusted computer, set ANDROID_TV_IP to the intended TV, confirm the device shown by adb devices, and disable debugging or revoke ADB authorization when finished. <br>


## Reference(s): <br>
- [ADB Keycode Reference](references/adb-keycodes.md) <br>
- [Android TV Netflix on ClawHub](https://clawhub.ai/jiayun/androidtv-netflix) <br>
- [Publisher Profile](https://clawhub.ai/user/jiayun) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ADB, an authorized Android TV connection, and a Netflix title ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
