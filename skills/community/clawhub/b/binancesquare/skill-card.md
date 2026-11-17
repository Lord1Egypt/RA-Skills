## Description:

Fetches Binance Square-style hot posts from the last 12 hours, filters out verified and institutional accounts, and prints content summaries, authors, timestamps, views, and comment counts in a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taibaiup](https://clawhub.ai/user/taibaiup)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to retrieve recent retail-discussion posts presented as Binance Square content, excluding verified users, special-role accounts, and authors with institution-like keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a non-obvious www.bmwweb.cc endpoint while presenting the returned data as Binance Square content.

Mitigation: Install only if this data source is acceptable; prefer a version that uses a documented official Binance endpoint or clearly discloses the third-party source.

Risk: Requests include fixed bnc-uid and Bnc-Uuid values.

Mitigation: Review and replace fixed identifiers before deployment, and avoid sending identifiers that should not be shared across users or environments.

Risk: Remote feed text is printed directly into terminal output.

Mitigation: Sanitize or escape remote text before displaying or reusing it in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taibaiup/skills/binancesquare)
- [Declared third-party feed endpoint](https://www.bmwweb.cc/bapi/composite/v9/friendly/pgc/feed/feed-recommend/list)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Plain text table suitable for Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints up to 15 filtered posts sorted by comment count.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
