## Description:

Cognitive Coach helps an agent ingest chat-history exports, extract high-value knowledge, create Feynman-style review cards, and prompt the user for next-day recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dearchenzj](https://clawhub.ai/user/dearchenzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technically curious users use this skill to turn dense AI chat histories into short Feynman-style review prompts and feedback that test whether they can explain important ideas in their own words.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes chat-history exports that may contain secrets, private third-party information, or content the user does not want retained.

Mitigation: Ask for consent before ingestion and instruct users to remove secrets and private third-party information before providing exports.

Risk: The skill silently extracts and stores review-card material, which can make it hard for users to see or control what was retained.

Mitigation: Show extracted topics or cards before storage and provide clear options to cancel ingestion or delete stored review cards.

Risk: The skill sets persistent next-morning review reminders without clear controls.

Mitigation: Confirm scheduled reminders with the user and provide a direct way to cancel or change the reminder.

## Reference(s):

- [Cognitive Coach ClawHub Skill Page](https://clawhub.ai/dearchenzj/skills/cognitivecoach)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Concise natural-language prompts and feedback, with internal review-card fields represented as structured text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create hidden review-card content and a next-morning reminder; proactive prompts should not reveal reference answers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
