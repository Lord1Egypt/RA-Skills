## Description:

Track bathroom events including pee, poop, and no-output attempts via chat, with local logging of time, duration, color, pain, Bristol stool scale, weekly summaries, and optional visual cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[herve-clawd](https://clawhub.ai/user/herve-clawd)

### License/Terms of Use:


## Use Case:

Individuals and agents use this skill to record bathroom events, monitor bowel and bladder patterns, summarize recent activity, and flag symptoms that may warrant professional medical advice. It is intended for personal tracking, not diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records private bathroom and symptom details in a local plaintext SQLite database.

Mitigation: Use it only on trusted devices, review local file permissions before deployment, and document deletion and retention expectations for users.

Risk: Optional card generation may create image files that contain sensitive bathroom details.

Mitigation: Keep cards disabled unless the user explicitly enables them, store generated cards in a private local directory, and avoid sharing generated media without review.

Risk: Command templates include user-provided notes and other free text.

Mitigation: Pass user-provided values as structured command arguments and avoid shell interpolation when invoking the CLI.

## Reference(s):

- [Bristol stool scale reference](references/bristol.md)
- [Optional card generation SOP](references/card_sop.md)
- [ClawHub skill page](https://clawhub.ai/herve-clawd/skills/excretion-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text with inline shell commands and JSON CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local SQLite records and optional PNG card images when visual cards are enabled.]

## Skill Version(s):

0.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
