## Description:

Scrape top ClickBank products by category with gravity scores, commission rates, and estimated monthly sales for affiliate marketing automation pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlowne12](https://clawhub.ai/user/marlowne12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and affiliate marketers use this skill to scrape public CBTrends ClickBank product rankings and produce JSON feeds for product comparison, Pinterest automation, affiliate performance tracking, or landing-page personalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper writes local JSON files that may include a user's ClickBank affiliate nickname in generated hoplinks.

Mitigation: Review output files before sharing, avoid committing generated output with a real affiliate nickname, and clean archived output periodically.

Risk: Automated scraping can become stale or fail if the public CBTrends page structure changes or if dependency versions drift.

Mitigation: Audit and pin npm dependencies before scheduled use, monitor scraper runs for empty or malformed results, and update parsing logic when source pages change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marlowne12/skills/clickbank-scraper)
- [Publisher profile](https://clawhub.ai/user/marlowne12)
- [CBTrends Health & Fitness source](https://www.cbtrends.com/browse-clickbank-marketplace/-1/94/Health%2B%2526%2BFitness/1/gravity/)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON files and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes latest and dated product snapshots under the local output directory; hoplinks may include the configured ClickBank affiliate nickname.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
