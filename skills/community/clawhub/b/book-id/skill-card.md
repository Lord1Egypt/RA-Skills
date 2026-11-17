## Description:

Catalog books from photos or text. Trigger on: book photo, catalog book, log book, add to library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabebac](https://clawhub.ai/user/gabebac)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal knowledge-base maintainers use this skill to identify books from cover photos or text, gather catalog metadata, and create structured book notes with associated cover images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to run shell commands against user-derived files and paths.

Mitigation: Review the skill before installation, trust the local fix-md.sh script before execution, and ensure generated filenames or inbound media names cannot inject shell syntax.

Risk: The skill can export generated notes to a vault destination after cataloging.

Mitigation: Confirm the vault push destination with the user before approving any export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gabebac/skills/book-id)
- [OpenLibrary Search API](https://openlibrary.org/search.json?title=[TITLE]&author=[AUTHOR]&limit=5)
- [OpenLibrary Covers API](https://covers.openlibrary.org/b/isbn/[ISBN]-M.jpg)
- [Wikipedia](https://www.wikipedia.org/)
- [Goodreads](https://www.goodreads.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown book note with YAML frontmatter, file paths, and confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 32-property book schema, a mandatory body section, a saved photo path, and an optional vault push prompt after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
