## Description: <br>
Automates copying DJI camera footage from an SD card or USB share to the next numbered backup folder on a NAS archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrazyFeng666](https://clawhub.ai/user/CrazyFeng666) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users who archive DJI camera footage use this skill to identify mounted media, create the next numbered NAS destination folder, and copy footage into it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may copy footage from the wrong mounted drive or into the wrong NAS folder when multiple drives are mounted. <br>
Mitigation: Confirm the detected source card or USB share and the newly created destination folder before copying files. <br>
Risk: The skill creates folders and copies files on mounted storage. <br>
Mitigation: Run it only when DJI footage backup to the configured NAS archive path is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrazyFeng666/dji-backup) <br>
- [Publisher profile](https://clawhub.ai/user/CrazyFeng666) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create numbered destination folders and copy files between mounted volumes when the user confirms the source and destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
