## Description:

Brand monitoring tool for tracking mentions across social media platforms, including Reddit, Google News, YouTube, and DuckDuckGo, with sentiment analysis, trend tracking, crisis detection, and competitor comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and brand operators use this skill to generate brand mention summaries, sentiment breakdowns, trend indicators, crisis alerts, competitor comparisons, and reporting guidance from configured brand keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill presents mostly demo or stub monitoring as real monitoring.

Mitigation: Treat generated reports as preliminary examples until live platform collection is implemented and verified against representative searches.

Risk: The security guidance warns against an unpinned global npx installer command.

Mitigation: Use a pinned, verifiable installer or inspect the package source before installation, and avoid elevated privileges for global installs.

Risk: Several scraper paths print notes to enable real API calls or RSS parsing before production use.

Mitigation: Validate each enabled platform connector, rate-limit handling, and source terms before relying on results for operational brand decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phheng/skills/ecommerce-brand-monitoring)
- [Publisher Profile](https://clawhub.ai/user/phheng)
- [Nexscope AI](https://www.nexscope.ai/)
- [Reddit Search JSON Endpoint](https://www.reddit.com)
- [Google News RSS Search](https://news.google.com/rss/search)
- [DuckDuckGo Instant Answer API](https://api.duckduckgo.com/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include sentiment summaries, alert recommendations, keyword lists, platform breakdowns, and competitor comparisons.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
