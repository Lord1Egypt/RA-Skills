## Description: <br>
Automatically checks version differences between local and online skills, with ClawHub/GitHub support and recurring update checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to track installed skills, compare local versions against online ClawHub or GitHub versions, and identify skills that may need updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update path can run shell commands and install remote code into the local skills workspace. <br>
Mitigation: Review the target skill name, publisher, and package source before using the update command. <br>
Risk: Recurring version checks may be configured through a cron entry. <br>
Mitigation: Confirm whether any scheduled job was added and disable it if recurring background checks are not wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/russellfei/catch-my-skill) <br>
- [GitHub repository link mentioned in README](https://github.com/russellfei/catch-my-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status reports with JSON tracking files and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local and online skill tracking data to JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
