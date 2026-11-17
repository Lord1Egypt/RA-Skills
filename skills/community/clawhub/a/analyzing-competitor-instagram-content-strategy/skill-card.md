## Description:

Analyzes a competitor's Instagram content strategy and performance using apidojo's Instagram scraper on Apify, returning post frequency, content mix, top-performing posts, hashtag strategy, and engagement benchmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, brand strategists, and content marketing teams use this skill to benchmark a competitor's Instagram content, engagement, posting cadence, and content gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify credentials can be exposed if tokens are pasted directly into commands or URLs.

Mitigation: Use a narrowly scoped APIFY_TOKEN from the environment or a credential-aware MCP/helper workflow, and avoid embedding tokens in command text.

Risk: Scraped Instagram handles and result datasets are sent to and stored by Apify according to its service behavior.

Mitigation: Use the skill only when Apify is an approved processor for the target analysis and when the scraped data handling is acceptable for the user's organization.

Risk: Small samples, scraper limits, or stale follower counts can make engagement benchmarks misleading.

Mitigation: Report the actual post count and date range, call out low sample sizes or scraper limits, and verify follower counts before drawing strategic conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/analyzing-competitor-instagram-content-strategy)
- [Server-Resolved GitHub Provenance](https://github.com/apidojo-io/apidojo-skills/tree/main/skills/intent/analyzing-competitor-instagram-content-strategy)
- [Apify actor: apidojo/instagram-scraper](https://apify.com/apidojo/instagram-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown strategy report with tables and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CSV or JSON file outputs when the Apify helper is used.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
