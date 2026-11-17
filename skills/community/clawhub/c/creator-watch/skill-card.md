## Description:

Creator Watch helps agents manage a curated Twitter/X creator watchlist, scrape public posts, import them to a local database, and analyze engagement and content patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research teams use this skill to track Twitter/X creators, update a local content database, and summarize patterns in high-performing posts for creator research and competitive intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scrape and update workflows may contact Twitter/X, encounter rate limits, and write records into a local database.

Mitigation: Use only trusted scraping and import scripts, confirm the intended creator scope before batch runs, and follow the documented rate-limiting strategy.

Risk: Analysis summaries may overstate patterns if the local database is incomplete, stale, or rate-limited.

Mitigation: Report scrape status, partial imports, and query scope alongside insights so users can judge evidence quality.

## Reference(s):

- [Creator Watch on ClawHub](https://clawhub.ai/phy041/skills/creator-watch)
- [Canlah AI](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include creator watchlists, scraping status tables, database schema, SQL queries, and analysis summaries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
