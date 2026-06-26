## Description: <br>
Helps manage Chinese birthday reminders by extracting birthdays from Chinese ID numbers, storing lunar or solar dates with per-record reminder lead times, and generating reminders for today or upcoming days. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web3aivc](https://clawhub.ai/user/web3aivc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain local birthday records, parse Chinese ID-card birthdays, convert between lunar and solar birthday dates, and produce upcoming reminder results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birthday records and optional Chinese ID-derived data may contain personal information stored locally. <br>
Mitigation: Avoid entering full ID numbers unless needed, review the generated birthdays.json file, and protect or remove local birthday data according to the user's privacy requirements. <br>
Risk: Email or webhook reminders can send birthday information to configured destinations. <br>
Mitigation: Keep non-agent channels disabled unless the destination is trusted, and review notification.json before enabling email or webhook delivery. <br>
Risk: Suggested daily automation may run reminder checks on a schedule. <br>
Mitigation: Approve the OpenClaw automation only after reviewing the command, schedule, and data file it will use. <br>


## Reference(s): <br>
- [Data format](references/data-format.md) <br>
- [ClawHub skill page](https://clawhub.ai/web3aivc/birthday) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores birthday records in local JSON and can emit an OpenClaw automation suggestion when the first record is created.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
