## Description:

EduClaw is a Chinese-language tutoring router that directs learners to English and math tutor agents with encouragement, scoring, and points-based practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohuiing](https://clawhub.ai/user/xiaohuiing)

### License/Terms of Use:

MIT-0

## Use Case:

Students use this skill for interactive elementary English and math practice, including word or sentence exercises, calculation practice, supportive feedback, scoring, and points-based motivation. Parents and guardians should review the subject-access and profile-memory behavior before use with children.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public docs do not clearly disclose the paid or private upgrade path for additional subjects.

Mitigation: Clearly state which subjects are free, which require authorization or payment, and what parent or guardian approval is needed before routing students to restricted subjects.

Risk: The skill may remember child profile details without stated privacy controls.

Mitigation: Limit stored child details to what tutoring requires, disclose retention behavior to parents or guardians, and provide review and deletion controls.

Risk: Math access can trigger an authorization or contact flow.

Mitigation: Make the authorization flow explicit and parent-directed before use, avoiding private contact instructions inside a child-facing tutoring exchange.

## Reference(s):

- [EduClaw ClawHub skill page](https://clawhub.ai/xiaohuiing/skills/edu-claw)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Conversational tutoring text with practice prompts, scoring feedback, and point updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable tool output; the included agent configs declare empty tool lists.]

## Skill Version(s):

2.44.0 (source: server release metadata; artifact VERSION.md states 2.43.0 and README.md states v2.29.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
