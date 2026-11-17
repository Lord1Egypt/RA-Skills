## Description:

Syncs Bunpro Japanese grammar learning progress from the community-documented frontend API into local storage for backups, progress tracking, review analysis, and JLPT insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mart1n-xyz](https://clawhub.ai/user/mart1n-xyz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to sync their Bunpro learning data to a local SQLite database and run reports over SRS stages, review forecasts, JLPT progress, due items, and leeches. It is intended for users who can provide a Bunpro frontend browser session token and manage the resulting local database privately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Bunpro frontend browser session token, which should be treated as account access until it expires or the session is revoked.

Mitigation: Use an environment variable for the token, avoid passing it on the command line on shared or logged systems, and revoke or refresh the browser session if exposure is suspected.

Risk: Synced data may include account profile details, learning progress, review history, and forecast data stored in a local SQLite database.

Mitigation: Store the database in a private directory and apply normal local data protection controls such as restricted file permissions and encrypted backups where appropriate.

Risk: The underlying Bunpro frontend API is community-documented and may change without notice, causing sync failures or incomplete reports.

Mitigation: Review errors before relying on reports, refresh the token when 401 responses occur, and re-check the referenced API documentation when endpoints fail.

## Reference(s):

- [Bunpro homepage](https://www.bunpro.jp)
- [Bunpro Community API GitHub](https://github.com/cbullard-dev/bunpro-community-api)
- [Bunpro Community Forum API Discussion](https://community.bunpro.jp/t/bunpro-api-when/100574)
- [Postman Collection](https://www.postman.com/technical-meteorologist-63813544/bunpro-api/collection/a7eufz9/bunpro-frontend-api)
- [Bunpro API Structure Reference](references/api-structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, SQL examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides Python scripts that call Bunpro endpoints and write reports from a local SQLite database.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
