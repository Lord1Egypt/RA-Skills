## Description: <br>
Calendar Manager helps an agent add, view, complete, delete, and summarize calendar events, reminders, holidays, memorable dates, and countdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using a Chinese-language personal productivity agent use this skill to manage daily schedules, reminders, holidays, anniversaries, countdowns, and lightweight time statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local calendar records may contain personal schedule details. <br>
Mitigation: Avoid storing secrets in event titles, locations, or notes, and keep local calendar files access-controlled. <br>
Risk: Calendar deletions are persistent and important schedule data could be lost. <br>
Mitigation: Keep backups for important calendar data before relying on the skill for ongoing schedule management. <br>
Risk: Natural-language time parsing is limited and may not capture all intended dates or times. <br>
Mitigation: Review event times after creation, especially for ambiguous requests or important reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/cp3d1455926-svg-calendar-manager) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill description](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown-like conversational text with local JSON event records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores schedule and memorable-day data in local JSON files.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
