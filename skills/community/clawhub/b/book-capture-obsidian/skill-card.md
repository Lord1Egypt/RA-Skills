## Description:

Catalogues photos, barcodes, ISBNs, titles and Goodreads exports as Obsidian book notes with covers, summaries and a library dashboard. Supports Google Books only, Open Library only, or both in either order. Use when the user wants to log or import books into Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodpalmeida](https://clawhub.ai/user/ricardodpalmeida)

### License/Terms of Use:

MIT-0

## Use Case:

Obsidian users can capture books from photos or ISBN and title lookups, import Goodreads exports, and organize their reading lists as notes and a library dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may write package caches outside the skill's virtual environment, and runtime permission limits were not verified.

Mitigation: Review setup behavior and run it with only the permissions you intend.

Risk: ISBNs, titles, and author names are sent to the selected metadata providers during lookups or enrichment.

Mitigation: Choose the provider mode deliberately; use --no-enrich for local Goodreads imports and keep API keys private.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ricardodpalmeida/skills/book-capture-obsidian)
- [Project homepage](https://github.com/Ricardodpalmeida/book-capture-obsidian-skill)
- [Configuration](references/configuration.md)
- [Data contracts](references/data-contracts.md)
- [Goodreads migration runbook](references/migration-runbook.md)
- [Google Books API documentation](https://developers.google.com/books/docs/v1/using#auth)
- [Open Library API documentation](https://openlibrary.org/developers/api)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Obsidian Markdown book notes and dashboard, with JSON workflow results and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes notes and dashboards to the selected Obsidian vault; dashboard queries require the Dataview plugin.]

## Skill Version(s):

1.4.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
