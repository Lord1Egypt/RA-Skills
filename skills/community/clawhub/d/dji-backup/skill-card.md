## Description:

Automates copying DJI camera footage from an SD card or USB share to the next numbered NAS backup folder for organized archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazyfeng666](https://clawhub.ai/user/crazyfeng666)

### License/Terms of Use:


## Use Case:

Developers and users managing DJI footage use this skill to guide an agent through copying mounted camera media into a numbered NAS archive folder after confirming source and destination paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create folders or copy a large amount of footage to the wrong location if mounted paths are misidentified.

Mitigation: Confirm that /Volumes/SD_Card/DCIM and /Volumes/File/DJI_Video are the intended locations, and have the agent show the planned source and destination before it creates folders or starts copying.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crazyfeng666/skills/dji-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with inline bash code blocks and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides source checks, destination folder selection, copy execution, and start/finish notifications.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
