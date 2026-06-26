## Description: <br>
Helps English learners record daily study check-ins for TOEFL, IELTS, PET, New Concept English, and similar study tracks, with support for non-repeating bilingual motivational quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daizongyu](https://clawhub.ai/user/daizongyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track daily English study progress, manage a selected study type, check status, and keep a local record of motivational quotes already used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a separate learning-checkin script selected by path or environment variable. <br>
Mitigation: Install only the intended learning-checkin skill, pass an explicit trusted learning_checkin.py path, and avoid setting LEARNING_CHECKIN_PATH in untrusted shells or project directories. <br>
Risk: The skill stores local progress configuration and quote-history data. <br>
Mitigation: Keep the skill data directory in a user-controlled location and review the stored JSON files if local study history should be removed or reset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daizongyu/english-learning-checkin) <br>
- [learning-checkin dependency](https://clawhub.ai/daizongyu/learning-checkin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains small local configuration and quote-history JSON files in the skill data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
