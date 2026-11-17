## Description:

Routes natural-language questions into a three-book answer experience and returns one random cited answer with minimal SQLite-backed per-user memory, duplicate-question protection, contextual book switching, and daily fortune support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaozrrr](https://clawhub.ai/user/shaozrrr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this Chinese-language text skill to ask open-ended questions and receive concise, cited responses drawn from movie, literature, or music answer-book corpora. Developers can also run, extend, or debug the local Python implementation and its SQLite-backed state flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the most recent question, answer, selected book, and timestamp in a local SQLite database.

Mitigation: Avoid entering secrets or highly sensitive personal details, and review, relocate, or delete the SQLite database when retained local state is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaozrrr/skills/book-of-answers-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [skill.json](artifact/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown-style conversational response with quoted answer text and citation source lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are selected from local movie, literature, and music answer corpora and may update minimal per-user SQLite state.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
