## Description:

Real-time competitive intelligence and market research using Bright Data's web scraping infrastructure, covering competitors' pricing, features, reviews, hiring patterns, content strategy, and market positioning with live web data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to gather live competitive and market intelligence, then synthesize it into competitor snapshots, pricing comparisons, review analyses, hiring-signal reports, content and SEO assessments, market landscape maps, and battlecards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install Bright Data CLI through a curl-to-bash command.

Mitigation: Do not run the installer blindly; prefer an official signed or package-manager install path, or download and verify the installer before executing it.

Risk: The skill depends on live web scraping and a Bright Data CLI login.

Mitigation: Install only where Bright Data use and CLI authentication are acceptable, and limit operation to explicit competitive-research requests.

Risk: Competitive intelligence reports can mislead users if scraped data is incomplete, gated, stale, or uncited.

Mitigation: Require source URLs, collection dates, clear gap disclosure, and separation between gathered facts and strategic interpretation.

## Reference(s):

- [Analysis Frameworks](references/analysis-frameworks.md)
- [Data Source Selection Guide](references/data-source-guide.md)
- [Industry Signal Interpretation Guide](references/industry-signals.md)
- [Output Templates](references/output-templates.md)
- [Bright Data CLI Installer](https://cli.brightdata.com/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, analysis, guidance]

**Output Format:** [Markdown reports with tables, source URLs, strategic recommendations, and inline Bright Data CLI commands where data collection is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should cite every data point, separate facts from analysis, state data collection date, and note unavailable or gated sources.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
