## Description:

CLI for AI agents to search and lookup books for their humans. Uses Open Library API. No auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent search Open Library for books, retrieve work details, and look up author biographies and bibliographies from command-line queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed package may be missing the referenced books scripts.

Mitigation: Verify that the package includes the books wrapper and scripts/books before relying on the skill.

Risk: The skill makes network requests to Open Library for public lookup data.

Mitigation: Use it only in environments where public Open Library requests are acceptable.

## Reference(s):

- [Open Library](https://openlibrary.org)
- [Open Library API](https://openlibrary.org/developers/api)
- [Publisher profile](https://clawhub.ai/user/jeffaf)
- [Skill page](https://clawhub.ai/jeffaf/skills/books)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include book search results, work metadata, author information, descriptions, subjects, ratings, and cover links from Open Library.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
