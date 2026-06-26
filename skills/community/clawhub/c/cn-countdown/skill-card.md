## Description: <br>
Cn Countdown helps Chinese-speaking users track countdowns, anniversaries, birthdays, exams, holidays, and other important dates from a local command-line utility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create, list, edit, delete, and calculate Chinese-language countdown or elapsed-day records for personal events. It is suited for local date tracking where event names, dates, tags, and notes remain on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Event names, dates, tags, and notes are saved locally in ~/.qclaw/workspace/countdown.json. <br>
Mitigation: Avoid storing sensitive personal details in event records, and use the edit/delete commands or remove the local data file when records are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-countdown) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Chinese-language terminal text with optional ANSI color and local JSON data records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores event records locally at ~/.qclaw/workspace/countdown.json.] <br>

## Skill Version(s): <br>
1.2.7 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
