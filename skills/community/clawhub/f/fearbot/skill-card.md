## Description:

CBT-based therapy for anxiety, depression, stress, and trauma. Provides structured cognitive behavioral therapy using Beck's model with validated clinical assessments (GAD-7, PHQ-9, DASS-21, PCL-5). Includes crisis detection, thought records, differential diagnosis, and session tracking. Activate with "therapy mode", "fearbot", or "start therapy".

This skill is ready for commercial/non-commercial use.

## Publisher:

[samoppakiks](https://clawhub.ai/user/samoppakiks)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to turn an OpenClaw agent into a structured CBT companion for mild-to-moderate anxiety, depression, stress, and trauma support. It guides intake and ongoing sessions, administers common screening instruments, tracks homework and thought records, and surfaces crisis resources when risk signals appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive therapy-related information may be stored locally, reused in future session context, or exported as plaintext.

Mitigation: Use only on a trusted machine with appropriate local storage permissions, avoid synced or shared directories, and review export paths before creating therapist-facing Markdown exports.

Risk: Crisis monitoring is described as broad message monitoring rather than limited to explicit therapy sessions.

Mitigation: Prefer deployment settings that scope monitoring to consented therapy interactions and provide clear controls for pausing monitoring and deleting records.

Risk: The skill provides mental-health support but is not a substitute for professional care or emergency services.

Mitigation: Keep professional referral and emergency/crisis-resource escalation prominent, especially for suicidality, psychosis, severe depression, substance abuse, eating disorders, bipolar disorder, or lack of improvement.

## Reference(s):

- [FearBot ClawHub listing](https://clawhub.ai/samoppakiks/skills/fearbot)
- [Assessment Administration Prompts](references/assessment-items.md)
- [Crisis Detection and Response Layer](references/crisis-layer.md)
- [Session Context Assembly Template](references/session-context-template.md)
- [Base Therapist System Prompt](references/therapist-prompt.md)
- [OpenClaw](https://openclaw.ai)
- [International Association for Suicide Prevention Crisis Centres](https://www.iasp.info/resources/Crisis_Centres/)
- [Befrienders Worldwide](https://www.befrienders.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown guidance with optional shell command output and Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local therapy session, assessment, mood, thought-record, homework, trigger, coping-strategy, and crisis-event data, and may export therapy history as Markdown.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
