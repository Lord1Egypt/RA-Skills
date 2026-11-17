## Description:

FeiFei Companion is a bilingual Trinity AI learning companion that routes K12 tutoring, study planning, learning reports, parent-child communication, and emotional support across three specialized tutor personas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonstang](https://clawhub.ai/user/simonstang)

### License/Terms of Use:

MIT-0

## Use Case:

Students, parents or guardians, and educators use this skill for bilingual K12 subject tutoring, personalized learning paths, learning reports, study planning, and parent-child communication support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks to build long-term profiles of children and share learning reports without clear privacy controls.

Mitigation: Use only with explicit student or guardian consent, minimize stored data, isolate each student profile, use short retention, and provide controls to disable or delete profiling.

Risk: Learning reports or parent-facing communications may expose sensitive student information or reach unintended recipients.

Mitigation: Require report previews, human approval before sharing, and verified parent or guardian recipients.

Risk: The security guidance identifies an AIGC-detection-evasion feature as inappropriate for use.

Mitigation: Remove the feature from the deployed skill or instruct agents to ignore it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/simonstang/skills/feifei-companion)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English responses; may include tutoring explanations, study plans, learner-profile summaries, reports, and parent-child communication drafts.]

## Skill Version(s):

4.0.0 (source: artifact/SKILL.md frontmatter; ClawHub release metadata version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
