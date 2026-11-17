## Description:

Guides users through an opt-in browser face scan and summarizes stress, mood, and heart-rate estimates, with optional analysis of user-provided media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gv66co](https://clawhub.ai/user/gv66co)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use the skill to request a face scan, compare readings before and after an activity, or play a consent-based group challenge. They can optionally submit their own photo or video for analysis with their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face and voice-derived readings are sensitive, and scanning others without their consent would compromise their privacy.

Mitigation: Run scans only at the user's request and only for the user or other consenting participants.

Risk: Stress and heart-rate estimates or game readings could be mistaken for medical findings or reliable judgments about a person.

Mitigation: Describe results as casual, non-medical estimates; do not use them for diagnosis or definitive claims about someone.

Risk: Optional photo or video analysis uploads sensitive media to EmoPulse through RapidAPI.

Mitigation: Disclose the upload and wait for explicit agreement; use only user-provided, consented media and the user's own environment-provided API key.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gv66co/skills/fitcheck-workout-readiness)
- [emo.city browser scan](https://emo.city?utm_source=clawhub&utm_medium=skill)
- [EmoPulse Face Analysis API](https://rapidapi.com/emocity/api/emopulse-face-analysis)
- [emo.city privacy policy](https://emo.city/privacy)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-language scan summary and structured JSON readings or comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a before-and-after comparison or a challenge scoreboard; missing heart-rate readings are null.]

## Skill Version(s):

1.5.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
