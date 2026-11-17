## Description:

Tracks intermittent and extended fasts by logging fast boundaries, calculating elapsed time and fasting stages, maintaining local preferences and history, and surfacing safety, electrolyte, refeeding, observance, training, and metric guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to track fasting start and break times, check current fasting status, plan common fasting protocols, and interpret fasting-related symptoms or metrics with safety guardrails. It is a logging and guidance skill, not a substitute for clinician-directed medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may keep fasting history, goals, symptoms, schedules, observance details, and preferences in local plaintext files.

Mitigation: Users should understand the local storage behavior before installing and avoid recording sensitive details they do not want stored under ~/Clawic/data/fasting/.

Risk: Fasting guidance can be unsafe for extended fasts, diabetes, pregnancy, eating-disorder history, medication interactions, or concerning symptoms.

Mitigation: Use clinician judgment for these situations; the skill should follow its red-flag routing and should not substitute for medical care.

## Reference(s):

- [ClawHub Fasting Tracker skill page](https://clawhub.ai/ivangdavila/skills/fasting)
- [Clawic Fasting Tracker homepage](https://clawic.com/skills/fasting)
- [Clawic skill library](https://clawic.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown responses with YAML and Markdown-backed local fasting records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local plaintext fasting configuration, log, and memory files under ~/Clawic/data/fasting/ when the user explicitly provides relevant fasting information.]

## Skill Version(s):

1.0.3 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
