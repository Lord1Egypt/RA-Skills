## Description: <br>
Calculates daily fortune readings from a birth date using Chinese lunar almanac signals, zodiac relationships, constellation scores, lucky elements, and practical advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaferliu](https://clawhub.ai/user/zaferliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or agents use this skill to request a daily fortune reading after supplying or saving a birthday. It returns love, career, wealth, health, and overall scores, along with lucky elements, almanac reminders, and concise advice for a selected date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the user's birthday locally for future calculations. <br>
Mitigation: Install only if local birthday storage is acceptable, and delete ~/.openclaw/fortune_birthday.json to remove the saved data. <br>
Risk: The skill depends on lunar-python for calendar calculations. <br>
Mitigation: Review or pin the lunar-python dependency before use in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zaferliu/fortune-luck) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Plain text or JSON fortune result with scores, lucky elements, calendar details, and advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can reuse a locally saved birthday from ~/.openclaw/fortune_birthday.json.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
