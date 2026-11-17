## Description:

Catalogues photos, barcodes, ISBNs, titles and Goodreads exports as Obsidian book notes with covers, summaries and a library dashboard. Supports Google Books only, Open Library only, or both in either order. Use when the user wants to log or import books into Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Obsidian users can capture books from photos, ISBNs, titles or Goodreads exports and maintain searchable book notes and a library dashboard. They can also enrich book metadata from Google Books or Open Library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance calls out external pip cache writes by the setup script and undeclared tool scope as items to review.

Mitigation: Before setup, inspect the script's cache paths and requested tool scope and confirm they fit the intended environment.

## Reference(s):

- [Configuration and metadata providers](references/configuration.md)
- [Book fields and data contracts](references/data-contracts.md)
- [Goodreads migration runbook](references/migration-runbook.md)
- [Troubleshooting](references/troubleshooting.md)
- [Google Books API documentation](https://developers.google.com/books/docs/v1/using#auth)
- [Open Library API documentation](https://openlibrary.org/developers/api)
- [Project homepage (metadata.clawdis homepage)](https://github.com/Ricardodpalmeida/book-capture-obsidian-skill)
- [ClawHub release page](https://clawhub.ai/ricardodpalmeida/skills/book-capture-obsidian)

## Skill Output:

**Output Type(s):** [Markdown, Files, JSON, Guidance]

**Output Format:** [Obsidian-compatible Markdown book notes and dashboard, with JSON operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes within the selected Obsidian vault; preserves user content below the User Notes section.]

## Skill Version(s):

1.4.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
