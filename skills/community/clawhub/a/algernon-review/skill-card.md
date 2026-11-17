## Description:

FSRS-4.5 flashcard review session for OpenAlgernon that handles flashcards, dissertative cards, argumentative cards, AI evaluation of open-ended answers, FSRS scheduling, N1/N2/N3 promotion, and correction card generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniovfranco](https://clawhub.ai/user/antoniovfranco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners using OpenAlgernon use this skill to run due-card review sessions, grade open-ended answers, update spaced-repetition scheduling, generate correction cards, and summarize review progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw SQLite instructions that include user, slug, ID, or AI-generated text may alter the local study database in unintended ways.

Mitigation: Review before installing, use parameterized SQLite operations, validate slugs and IDs, and escape generated text safely.

Risk: The skill appends review-session details to a local conversation log, which may expose study activity or sensitive material metadata.

Mitigation: Document the logging behavior clearly and make the conversation-log append optional when study data is sensitive.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with interactive prompts, feedback text, and inline SQLite shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review-session summaries and may propose local SQLite updates and conversation-log appends.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
