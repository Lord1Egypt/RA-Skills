## Description:

Generates Chinese meeting summaries, extracts action items, coordinates meeting scheduling prompts, and provides reusable meeting templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to convert meeting notes into structured minutes, extract owners and deadlines, review meeting templates, and inspect scheduled meeting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting content may be saved locally as plaintext JSON, including attendee names, notes, decisions, action items, and schedule details.

Mitigation: Use the skill only where local plaintext storage is acceptable, avoid highly confidential meetings, and define retention and deletion practices before deployment.

Risk: Generated minutes and extracted action items may omit context or assign incorrect ownership or deadlines.

Mitigation: Have a meeting owner review generated summaries and task lists before sharing them or using them for follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/cp3d1455926-svg-meeting-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Chinese-language Markdown-style text responses and local JSON meeting records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save meeting content, attendee names, action items, and schedule details as plaintext JSON in the skill artifact directory.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact SKILL.md lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
