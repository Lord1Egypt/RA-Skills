## Description: <br>
A local calendar memo skill for adding, viewing, completing, and deleting personal todos and schedule reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiyuxi24](https://clawhub.ai/user/qiyuxi24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using OpenClaw can manage a personal local schedule by adding tasks, checking today's or upcoming items, and marking items complete or deleted. The skill can also send reminder notifications before scheduled events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic Feishu reminder pushes may send schedule text outside the local memo context without clear install-time consent. <br>
Mitigation: Install only when Feishu reminder delivery is intended, and avoid sensitive schedule details unless explicit opt-in and disable controls are added. <br>
Risk: Reminder text is passed through a shell command when sending notifications. <br>
Mitigation: Review the skill before installation and prefer safer argument-based command execution before handling untrusted or sensitive entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiyuxi24/calender-memo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Text and Markdown replies, local JSON event records, and configured reminder messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores schedule data locally and checks for reminders periodically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
