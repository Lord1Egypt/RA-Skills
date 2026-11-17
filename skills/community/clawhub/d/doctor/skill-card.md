## Description:

Doctor helps an agent triage health questions, interpret labs and medication safety issues, and produce urgency-focused guidance with clear escalation tripwires.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Doctor through an agent to get urgency-oriented health guidance for symptoms, lab results, medications, chronic conditions, appointments, prevention, child health, mental health, reproductive health, and older-adult concerns. The skill is intended to help decide when to seek care and what to tell a clinician, not to diagnose or change prescription-only treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles very sensitive health information and defaults to reading and persistently updating local medical records.

Mitigation: Review before installation, use health_logging: minimal or health_logging: off when durable records are not wanted, and require manual approval before reads, writes, moves, or deletions if local health-record updates are a concern.

Risk: Health guidance can be harmful if emergency warning signs are missed or reassurance is too broad.

Mitigation: Keep red-flag escalation first, answer in urgency windows with explicit tripwires, and route diagnosis or prescription decisions to a qualified clinician.

Risk: Medication advice may be unsafe if allergies, current medicines, pregnancy status, kidney or liver status, or existing conditions are not considered.

Mitigation: Read the stored health profile before naming any drug or dose, avoid initiating or changing prescription-only medicine, and frame medication changes as questions for the prescriber or pharmacist.

## Reference(s):

- [Doctor ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/doctor)
- [Doctor Clawic Skill Page](https://clawic.com/skills/doctor)
- [Clawic Skill Library](https://clawic.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files, Configuration]

**Output Format:** [Markdown or plain text health guidance with optional local note updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local Clawic health notes when health_logging is enabled; credentials are represented as pointers rather than stored values.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
