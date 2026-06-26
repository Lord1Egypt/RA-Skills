## Description: <br>
Deepfocus provides a Bash-based local productivity logger for tasks, plans, reviews, streaks, reminders, searches, status checks, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use Deepfocus through an agent or terminal to capture lightweight productivity notes, task plans, habit streaks, reminders, reviews, and exports in local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Productivity entries are stored in plaintext under ~/.local/share/deepfocus. <br>
Mitigation: Do not store passwords, API keys, private credentials, or highly sensitive notes in Deepfocus logs. <br>
Risk: The Pomodoro timer wording is broader than the submitted script behavior. <br>
Mitigation: Treat the release as a local task and note tracker unless timer functionality is verified in a later artifact. <br>
Risk: The skill runs a local Bash script that writes files in the user's home directory. <br>
Mitigation: Review the script before use and run it only with user-level permissions in an environment where local plaintext logs are acceptable. <br>


## Reference(s): <br>
- [Deepfocus ClawHub skill page](https://clawhub.ai/bytesagain-lab/deepfocus) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, files, configuration] <br>
**Output Format:** [Terminal text plus local log files and export files in JSON, CSV, or TXT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores plaintext productivity entries under ~/.local/share/deepfocus and uses Bash with standard coreutils.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
