## Description:

Compares theatrical film grosses using Crawlora Box Office Mojo charts, title and release records, and stored data while preserving reporting scope and sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, developers, and other users can compare film grosses across titles, release windows, markets, or franchises, with consistent measures and source dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora queries and the API key are sent to Crawlora's API.

Mitigation: Use a key kept in CRAWLORA_API_KEY; do not commit it or paste it into shared logs, and only send queries you are comfortable sharing.

Risk: Searches may consume API credits.

Mitigation: Limit query scope and page counts to the comparison needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/film-box-office-comparison)
- [Endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison tables and prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes title and release identities, gross basis, source dates, formulas, and coverage gaps.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
