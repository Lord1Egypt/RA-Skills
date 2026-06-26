## Description: <br>
Guides an agent through blood-pressure profile collection, reading classification, warning prompts, and optional non-drug audio wellness recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hcrunner](https://clawhub.ai/user/hcrunner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using an agent for blood-pressure self-management can use this skill to collect a basic profile, record readings, classify them against AHA/ACC-style thresholds, and receive wellness-oriented follow-up guidance. It should be treated as adjunct health guidance, not diagnosis or replacement for clinician-directed care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to collect and remember sensitive blood-pressure profile information. <br>
Mitigation: Collect only necessary health details, obtain clear user consent before long-term storage, and make deletion or review of stored profile data available. <br>
Risk: The audio recommendation and therapy claims could be mistaken for medical treatment. <br>
Mitigation: Present the audio as a wellness aid only, continue clinician-prescribed care, and seek urgent medical help for very high readings or concerning symptoms. <br>
Risk: Blood-pressure readings and classifications may be incomplete or user-entered incorrectly. <br>
Mitigation: Ask users to verify measurements, repeat readings when appropriate, and consult qualified clinicians for diagnosis, treatment, or medication decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hcrunner/blood-pressure-therapy) <br>
- [AHA/ACC 2017 Blood Pressure Reference](references/AHA_ACC_2017.md) <br>
- [Audio Intervention Principle Reference](references/principle.md) <br>
- [Therapy Audio Link](https://myxt.com/link/738cba02-d41a-453a-99db-9be5545c1cd7) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, json, files] <br>
**Output Format:** [Conversational Markdown with optional JSON profile data and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask one profile question at a time, evaluate user-supplied blood-pressure readings, and recommend urgent care for crisis-level readings.] <br>

## Skill Version(s): <br>
3.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
