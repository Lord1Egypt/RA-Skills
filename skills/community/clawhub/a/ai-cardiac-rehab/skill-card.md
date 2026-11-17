## Description:

AI-Cardiac-Rehab is a cardiac rehabilitation management web app that supports symptom alerts, risk stratification, individualized exercise guidance, medication adherence reminders, and local patient records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-feng123](https://clawhub.ai/user/chen-feng123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and healthcare-adjacent developers use this skill to run a local cardiac rehabilitation support app for patient profile tracking, daily logs, safety alerts, risk stratification, exercise guidance, and medication reminders. Recommendations should be reviewed by a qualified clinician before use with patients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive medical data and stores patient profile and daily log information locally.

Mitigation: Use strong local data protections, access controls, backup controls, and deployment review before using it with sensitive health records.

Risk: Exercise guidance and risk stratification may be interpreted as medical authority.

Mitigation: Treat outputs as experimental decision support and require qualified clinician review before a patient follows any rehabilitation plan.

Risk: Emergency symptom matching may miss clinically relevant wording.

Mitigation: Use a clinician-reviewed symptom vocabulary and validate emergency stop behavior before deployment.

Risk: Unpinned dependencies and third-party frontend assets can change over time or disclose client requests.

Mitigation: Pin dependencies, self-host frontend assets where practical, or clearly disclose any third-party requests before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen-feng123/skills/ai-cardiac-rehab)
- [API specification](artifact/API_SPEC.md)
- [Use guide](artifact/USE_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration, Shell commands]

**Output Format:** [Web UI text with Markdown documentation and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces risk level, exercise intensity, target heart-rate range, exercise guidance, medication reminders, monitoring tips, and safety warnings from patient profile and daily log inputs.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
