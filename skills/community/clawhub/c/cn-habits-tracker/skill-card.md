## Description: <br>
Cn Habits Tracker helps agents guide Chinese-language habit tracking through a local Python CLI for adding habits, daily check-ins, streaks, reminders, and weekly or monthly reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use this skill to manage personal habit tracking in Chinese, including local check-ins, habit lists, reminders, streak summaries, and progress reports. It is suited for local productivity workflows where user-entered habit data remains on the device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Habit names, notes, amounts, and check-in history are stored locally and may contain personal routine information. <br>
Mitigation: Review the local JSON data file before sharing the device, workspace, backups, or logs. <br>
Risk: The README includes promotional links unrelated to the local tracking script. <br>
Mitigation: Treat promotional links as optional external websites; the script itself showed no evidence of network access in the security evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-habits-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script stores habit names, notes, amounts, and check-in history in a local JSON file at ~/.qclaw/workspace/habits.json.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
