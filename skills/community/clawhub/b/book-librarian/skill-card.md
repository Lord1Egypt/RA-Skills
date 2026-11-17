## Description:

Manage reading life: recommend books, track reads, move wishlist to library, and suggest what to read next based on mood.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perplexingperfectionist](https://clawhub.ai/user/perplexingperfectionist)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal reading companion to track owned books, maintain a wishlist, log reading reactions, and get spoiler-free recommendations based on mood and taste.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain a local history of books, wishlist entries, moods, ratings, and taste notes.

Mitigation: Review the generated books/ files and memory/library.md periodically, and delete them if you do not want that reading history retained.

Risk: Recommendations and reading-profile updates may reflect incomplete or outdated user taste notes.

Mitigation: Review recommendation rationale and update memory/library.md when preferences change or a suggestion does not fit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/perplexingperfectionist/skills/book-librarian)
- [README](artifact/README.md)
- [Library Template](artifact/templates/library.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Concise Markdown responses with local CSV and Markdown file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spoiler-free recommendations; stores reading history, wishlist entries, mood map, ratings, and taste notes locally when the user permits setup.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
