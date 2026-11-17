## Description:

Recommend books based on interests or reading history, provide book details and ratings from the bundled catalog, and help manage reading lists and notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-language users can ask an agent for book recommendations, book searches, reading-list management, and reading statistics. Developers and operators can use the skill as a compact local book-helper capability with JSON-backed notes and bookshelf state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store reading lists, progress, and notes in local JSON files.

Mitigation: Avoid entering sensitive personal reflections unless users understand where the files are stored and how to remove them.

Risk: Book ratings and details are drawn from bundled catalog data rather than a verified live source in the artifact.

Mitigation: Verify ratings, reviews, and bibliographic details before relying on them for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/book-recommender)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown text responses with book recommendations, book details, bookshelf summaries, reading notes, and reading statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local JSON files for bookshelf and reading-note state.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
