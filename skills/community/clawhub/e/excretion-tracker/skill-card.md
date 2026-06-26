## Description: <br>
Track bathroom events (pee/poop) via chat: start time, duration, color, pain, and Bristol stool scale. Generates weekly summaries and optional constipation reminders when no poop occurs past a threshold (default 24h, user-configurable). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[herve-clawd](https://clawhub.ai/user/herve-clawd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to log pee, poop, and no-output bathroom attempts through chat, keep a local bathroom history, and review weekly bowel and bladder patterns. It supports symptom tracking but does not provide medical diagnosis or medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bathroom logs can contain sensitive personal health information stored on the user's device. <br>
Mitigation: Install only when comfortable storing these logs locally, and avoid sharing the local database or generated summaries with untrusted parties. <br>
Risk: Optional visual card generation may use selected event details to create local images through a separate skill. <br>
Mitigation: Keep card generation disabled unless the separate nano-banana-pro skill is trusted and the user is comfortable with those details being used for image creation. <br>
Risk: Users could mistake bathroom trend summaries for medical guidance. <br>
Mitigation: Present summaries as logs only, include the not-medical-advice note, and recommend professional medical advice for blood, severe pain, fever, or symptoms lasting more than 24 to 48 hours. <br>


## Reference(s): <br>
- [Bristol stool scale](references/bristol.md) <br>
- [Card generation SOP](references/card_sop.md) <br>
- [ClawHub skill page](https://clawhub.ai/herve-clawd/excretion-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chat responses with inline shell commands and JSON CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores bathroom logs locally in SQLite; optional image card generation is disabled by default and depends on a separate user-installed skill.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
