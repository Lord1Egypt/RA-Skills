## Description: <br>
纪念日管理 helps users manage birthdays, anniversaries, memorial dates, ancestor worship dates, lunar and solar calendar conversions, solar terms, holiday countdowns, and date calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chanvging](https://clawhub.ai/user/chanvging) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and assistants use this skill to keep a local record of important personal dates, find upcoming reminders, and answer calendar questions involving birthdays, anniversaries, memorial days, lunar dates, solar terms, and holidays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal dates, relationships, and notes in a local JSON file under the skill directory. <br>
Mitigation: Use it only where local storage of that information is acceptable, and avoid recording sensitive details beyond what is needed. <br>
Risk: Delete commands remove date records without an undo flow. <br>
Mitigation: Review records with list or get before deleting, and keep a backup of dates.json when preserving history matters. <br>
Risk: Optional Python dependencies affect lunar conversion and solar-term precision. <br>
Mitigation: Review dependencies before installing them, and treat fallback solar-term dates as approximate when chinese-calendar is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chanvging/date-manager) <br>
- [Publisher profile](https://clawhub.ai/user/chanvging) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python CLI commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update a local data/dates.json file under the skill directory; optional zhdate and chinese-calendar dependencies improve lunar and solar-term accuracy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
