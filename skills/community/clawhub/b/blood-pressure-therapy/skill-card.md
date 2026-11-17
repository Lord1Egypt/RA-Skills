## Description:

A Chinese-language health management skill for people monitoring elevated blood pressure that collects profile and blood-pressure inputs, classifies readings, flags urgent values, and recommends a non-drug audio intervention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hcrunner](https://clawhub.ai/user/hcrunner)

### License/Terms of Use:

MIT-0

## Use Case:

External users with elevated blood-pressure concerns use this skill to record health profile factors, classify self-reported blood-pressure readings, receive warning language for concerning values, and access a referenced wellness audio link. It is an assistive wellness workflow and should not replace clinician advice, medication, urgent care, or validated blood-pressure monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and stores sensitive health profile and blood-pressure information in a local file and long-term agent memory.

Mitigation: Use only with explicit user consent, avoid entering unnecessary health details, and provide a clear process to review, update, or delete stored profile data.

Risk: The skill makes strong wellness claims for an audio intervention related to blood-pressure reduction.

Mitigation: Present the audio as unverified wellness content and clearly state that it is not a substitute for medication, clinician advice, urgent care, or validated blood-pressure monitoring.

Risk: Users with very high or rapidly worsening blood-pressure readings could delay appropriate medical care.

Mitigation: Preserve urgent-care warnings for hypertensive crisis ranges and direct users with severe readings or symptoms to seek immediate medical attention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hcrunner/skills/blood-pressure-therapy)
- [AHA/ACC 2017 blood pressure classification reference](references/AHA_ACC_2017.md)
- [Audio intervention principle reference](references/principle.md)
- [Profile intake fields](api/profile_inquired.md)
- [Referenced hypertension audio link](https://myxt.com/link/738cba02-d41a-453a-99db-9be5545c1cd7)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Conversational Markdown with optional pretty-printed JSON profile data and an external audio URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update hc_profile.md and request long-term memory storage of health profile details.]

## Skill Version(s):

3.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
