## Description: <br>
Dating intelligence co-pilot that helps users remember details, preferences, important dates, and reflections about people they are dating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a private dating memory assistant to record their own observations after dates, refresh themselves before future dates, and generate thoughtful ideas based on details they manually entered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create sensitive plain-text notes about people the user dates. <br>
Mitigation: Keep notes local, protect the device or account where they are stored, and avoid recording unnecessary sensitive details. <br>
Risk: Retaining dating profiles after a relationship ends can create unnecessary privacy exposure. <br>
Mitigation: Delete profiles that are no longer needed, as recommended by the artifact and security guidance. <br>
Risk: Using remembered details to monitor, manipulate, or pressure another person would violate the skill's stated posture. <br>
Mitigation: Use only information shared appropriately in normal conversation and decline surveillance, stalking, or manipulation requests. <br>


## Reference(s): <br>
- [Date.skill ClawHub page](https://clawhub.ai/realteamprinz/date) <br>
- [Date profile template](templates/DATE-PROFILE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and plain-text guidance with local profile and date-log file structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Markdown and JSONL notes under ~/.date-skill/people/ when the agent follows the documented storage pattern.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
