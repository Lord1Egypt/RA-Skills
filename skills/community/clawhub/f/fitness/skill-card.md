## Description:

Plans and progresses workout programs — strength, muscle building, cardio, endurance, and general conditioning — with quantified rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to design, adjust, and progress fitness training plans for strength, muscle gain, cardio, endurance, body composition, return-to-training, and limited-equipment scenarios. It also helps interpret workout logs and wearable readiness signals into concrete next-session guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive workout and health details may be stored as plaintext local records.

Mitigation: Use the skill only when local persistence is acceptable; restrict file permissions, avoid cloud sync for the fitness data folder, and periodically review or delete stored records.

Risk: Exercise guidance can be inappropriate when pain, illness, pregnancy, or cardiac, metabolic, or renal conditions are present.

Mitigation: Apply the skill's red-flag and clinician-clearance gates before new vigorous programming, and keep guidance conservative when escalation criteria are present.

Risk: Wearable readiness scores and trend data can be noisy or misleading.

Mitigation: Base program changes on raw resting heart rate, sleep, logged performance, and the skill's canonical triggers rather than proprietary readiness scores alone.

## Reference(s):

- [ClawHub Fitness skill page](https://clawhub.ai/ivangdavila/skills/fitness)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic Fitness skill page](https://clawic.com/skills/fitness)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured training prescriptions and optional local configuration or log updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reuse plaintext fitness records under ~/Clawic/data/fitness/ when the host agent follows the skill's persistence guidance.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
