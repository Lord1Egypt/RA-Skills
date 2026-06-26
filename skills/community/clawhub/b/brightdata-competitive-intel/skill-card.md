## Description: <br>
Real-time competitive intelligence and market research using Bright Data's web scraping infrastructure to analyze competitors' pricing, features, reviews, hiring patterns, content strategy, and market positioning with live web data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and business teams use this skill to gather live competitive and market data with Bright Data and turn it into sourced competitor snapshots, pricing comparisons, review intelligence, hiring-signal analysis, SEO/content analysis, market landscape maps, and battlecards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Competitive research queries, target URLs, and market interests may be sent to Bright Data during data collection. <br>
Mitigation: Avoid confidential internal strategy in scraping queries and review what will be collected before running Bright Data commands. <br>
Risk: Bright Data usage can incur account costs when broad competitive deep dives run many collection calls. <br>
Mitigation: Use a quota-limited Bright Data account where possible and set a budget or call limit before running broad research. <br>
Risk: The skill installs and relies on the Bright Data CLI from an external installer URL. <br>
Mitigation: Verify the CLI installer source before installation and use the documented one-time login flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meirk-brd/brightdata-competitive-intel) <br>
- [Bright Data CLI installer](https://cli.brightdata.com/install.sh) <br>
- [Analysis Frameworks](references/analysis-frameworks.md) <br>
- [Data Source Guide](references/data-source-guide.md) <br>
- [Industry Signals](references/industry-signals.md) <br>
- [Output Templates](references/output-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with sourced findings, comparison tables, strategic recommendations, and inline shell commands for Bright Data collection.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite source URLs, separate facts from analysis, date-stamp collected data, and identify gaps when live data is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
