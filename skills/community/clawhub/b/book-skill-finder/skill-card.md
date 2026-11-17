## Description:

Book Skill Finder helps agents search a bundled nonfiction book dataset and return ratings, summaries, book links, and suggested knowledge-file additions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaysonmeng](https://clawhub.ai/user/jaysonmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find nonfiction books by title, author, or concept and to draft knowledge-base additions for agents from selected book summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned ratings and summaries come from the bundled Heardly/local dataset and may not match live Goodreads data or current external records.

Mitigation: Present ratings as local dataset scores and verify important book details against an authoritative source before relying on them.

Risk: Generated SOUL, MEMORY, and SKILL snippets could add inaccurate or unwanted content to an agent knowledge base if applied directly.

Mitigation: Review and edit generated snippets before manually adding them to agent knowledge files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaysonmeng/skills/book-skill-finder)
- [Heardly Book Links](https://heardly.app/book)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON-like JavaScript objects with Markdown snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local dataset search; search() defaults to a maximum of 5 results.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
