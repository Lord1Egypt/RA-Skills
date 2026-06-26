## Description: <br>
A personalized fitness coach and nutrition guide tailored for life in Dubai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadmanshaikh](https://clawhub.ai/user/shadmanshaikh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to build a Dubai-localized fitness profile, receive personalized training plans, get nutrition guidance, and track progress toward fitness events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists sensitive personal fitness and body-profile data in local Markdown memory files. <br>
Mitigation: Confirm consent before saving body metrics, diet details, location, or progress history; clearly identify the local files used; and honor review, update, and deletion requests. <br>
Risk: Retained local profile data may remain after the user no longer wants the skill to remember it. <br>
Mitigation: Review or delete user_memory.md and coach.md when retention is no longer desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shadmanshaikh/fit-dubai) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Profile instructions](artifact/profile.md) <br>
- [Dubai fitness coach plan](artifact/coach.md) <br>
- [Nutrition guide](artifact/nutrition.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Conversational guidance and Markdown profile, training, nutrition, and progress notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local Markdown memory files with fitness profile, body metrics, location, dietary preferences, goals, and progress history.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
