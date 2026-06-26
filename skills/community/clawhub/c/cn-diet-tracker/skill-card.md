## Description: <br>
Cn Diet Tracker helps agents guide Chinese-speaking users through local meal logging, calorie summaries, weekly reports, and daily calorie target management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users and agents use this skill to record meals with calorie estimates, review daily or weekly intake, and manage a daily calorie target using local data storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food, calorie, timestamp, and note data is stored unencrypted in a local JSON file. <br>
Mitigation: Use only on trusted devices, avoid shared or synced home directories, and delete ~/.qclaw/workspace/diet.json when records should be removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-diet-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local diet records at ~/.qclaw/workspace/diet.json when the user runs the tracking command.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
