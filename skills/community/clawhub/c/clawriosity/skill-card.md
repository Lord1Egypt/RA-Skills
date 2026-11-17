## Description:

Daily curiosity feed from AIgneous Million Whys that lets users query science and culture questions by topic or semantic search and receive quizzes, articles, flashcards, or podcast scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyc11776611](https://clawhub.ai/user/lyc11776611)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal curiosity feed for science and culture questions, with adaptive quiz, article, flashcard, and podcast-style outputs. It also supports community question contributions and topic suggestions when the user gives consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends query topics and contribution content to millionwhys.com.

Mitigation: Avoid sensitive personal topics and review outbound query or contribution content before submission.

Risk: The skill asks the agent to store an API key and maintain a persistent interest profile.

Mitigation: Use secure credential storage, provide a clear removal process, and let users opt out of remembered preferences where the host agent supports it.

Risk: Community contributions could submit user-provided facts or suggestions externally.

Mitigation: Fact-check proposed contributions, obtain explicit user consent, and avoid submitting personal or sensitive information.

## Reference(s):

- [Clawriosity ClawHub Skill Page](https://clawhub.ai/lyc11776611/skills/clawriosity)
- [Million Whys](https://millionwhys.com)
- [Million Whys OpenClaw API](https://millionwhys.com/api/openclaw)
- [Million Whys Query API](https://millionwhys.com/api/openclaw/query)
- [Million Whys Register API](https://millionwhys.com/api/openclaw/register)
- [Million Whys Contribution API](https://millionwhys.com/api/openclaw/contribute)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline images, quiz cards, article cards, flashcards, podcast scripts, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual English or Chinese content, translated presentation for other user languages, quota notices, and remembered question IDs or interests for personalization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
