## Description: <br>
Provides countdown management, important-date reminders, Pomodoro timers, and custom reminder support for an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask the agent to calculate days until events, record birthdays or anniversaries, view saved countdowns, start a Pomodoro work timer, or set simple reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Countdown names, birthdays, anniversaries, and reminder labels are saved locally in JSON data. <br>
Mitigation: Avoid storing sensitive labels or personal details unless the local storage location and access controls are acceptable. <br>
Risk: Documentation and implementation describe different countdowns.json storage locations. <br>
Mitigation: Confirm the actual local file path before relying on privacy, backup, or cleanup assumptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/countdown-timer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown text responses with countdown lists, timer confirmations, and reminder status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local JSON countdown data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
