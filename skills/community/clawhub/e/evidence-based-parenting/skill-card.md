## Description:

摸摸头（PatPat） is a Simplified Chinese parenting-coach skill that helps caregivers handle 0-15 year-old parenting scenarios with age-aware, safety-routed, practical guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gglinux](https://clawhub.ai/user/gglinux)

### License/Terms of Use:

MIT-0

## Use Case:

External parents and caregivers use this skill for general educational support across common parenting challenges, including emotion regulation, behavior guidance, learning support, social issues, adolescent communication, and caregiver self-support. The skill routes each request by age range, scenario, timing, safety level, and caregiver state before producing concise Simplified Chinese guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat parenting guidance as medical, psychological, legal, or emergency help.

Mitigation: Present the skill as general educational support and direct users to qualified professional or emergency support for self-harm, abuse, violence, severe withdrawal, persistent impairment, or other urgent safety issues.

Risk: Guidance may be mismatched when the child's age, situation timing, safety level, or caregiver state is unclear.

Mitigation: Use the artifact's routing flow and ask one concise clarifying question when key context cannot be inferred.

Risk: Family conflict or child safety scenarios can require immediate intervention rather than routine coaching.

Mitigation: Apply the artifact's green/yellow/red safety triage and stop normal coaching when red-risk signals appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gglinux/skills/evidence-based-parenting)
- [Publisher profile](https://clawhub.ai/user/gglinux)
- [README](artifact/README.md)
- [Project vision](artifact/VISION.md)
- [Skill instructions](artifact/SKILL.md)
- [Age routing engine](artifact/logic/age-engine.md)
- [Story and interaction framework](artifact/logic/story-engine.md)
- [Parent coaching framework](artifact/logic/parent-coach.md)
- [Emotion and body-signal mapping](artifact/logic/emotion-creatures.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Simplified Chinese Markdown guidance, with optional structured response fields when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, persistence, credential access, or external data handling is described in the release evidence.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
