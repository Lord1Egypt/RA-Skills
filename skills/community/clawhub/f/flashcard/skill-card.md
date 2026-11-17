## Description:

Spaced repetition study tool with deck management. Use when you need flashcard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, review, quiz, export, and plan flashcard-based study workflows with spaced repetition guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises deck-managed flashcards, but the shipped scripts include broader study-helper commands and behavior.

Mitigation: Review the available commands against the intended workflow before installing or exposing the skill to users.

Risk: One script stores local notes and history in a flashcard data directory.

Mitigation: Use an explicit local data directory and avoid entering sensitive study notes unless local retention is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/flashcard)
- [Publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples and study templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated flashcards, review plans, quizzes, export formats, statistics reports, and local shell command output.]

## Skill Version(s):

2.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
