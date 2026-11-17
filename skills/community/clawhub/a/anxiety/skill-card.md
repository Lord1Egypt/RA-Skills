## Description:

Track anxiety episodes, triggers, thoughts, and coping responses with therapy-ready logs, weekly trend reviews, and safety-first escalation cues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to track anxiety symptoms, panic episodes, worry spirals, avoidance patterns, and coping outcomes. The skill helps agents create therapy-ready local Markdown logs, trigger maps, weekly reviews, coping plans, thought records, exposure ladders, and escalation cues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create sensitive anxiety logs, thought records, trigger maps, exposure notes, and escalation preferences in local Markdown files.

Mitigation: Use local storage only when the user is comfortable with it, ask before writing files, restrict file permissions, avoid cloud-synced folders, and delete records that are no longer needed.

Risk: Users may present self-harm, severe panic, medical red flags, or substance-related crisis signals that are outside routine tracking and coping support.

Mitigation: Follow the triage rules first: prioritize urgent safety guidance, route to emergency or professional care when red flags appear, and pause routine coaching and tracking.

Risk: Mental health tracking guidance could be mistaken for diagnosis or emergency treatment.

Mitigation: Keep the skill scoped to tracking and behavior-change planning, avoid diagnostic claims, and encourage professional follow-up for amber or red flags.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/anxiety)
- [Skill homepage](https://clawic.com/skills/anxiety)
- [Setup guidance](artifact/setup.md)
- [Memory template](artifact/memory-template.md)
- [Tracking modes](artifact/tracking-modes.md)
- [Anxiety event logging template](artifact/event-log-template.md)
- [Thought record workflow](artifact/thought-record.md)
- [Regulation playbook](artifact/regulation-playbook.md)
- [Graded exposure ladder](artifact/exposure-ladder.md)
- [Weekly review rules](artifact/weekly-review.md)
- [Triage rules](artifact/triage-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown notes, templates, plans, summaries, and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local Markdown records under ~/anxiety/ only after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
