## Description:

Scrapes Amazon.com rankings, search results, and product pages for marketplace analysis using Docker and Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace analysts use this skill to collect Amazon product, ranking, and search data for product research, competitor analysis, and price monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid proxies can incur metered costs and expose proxy credentials if mishandled.

Mitigation: Use dedicated proxy credentials, pass them at runtime rather than in shared files or command text, and limit unnecessary runs.

Risk: Optional browser control can access an authenticated Amazon session.

Mitigation: Use a dedicated Amazon account and keep Chrome's debugging interface bound to 127.0.0.1; never expose it publicly.

Risk: Generic mode can scrape arbitrary websites beyond the intended Amazon use case.

Mitigation: Avoid generic mode unless the user explicitly intends to scrape another site for an Amazon-related task.

Risk: Saved scraping state can retain account or browsing data.

Mitigation: Protect local scrape output and browser state, and remove stored data when no longer needed.

## Reference(s):

- [Amazon Scraper on ClawHub](https://clawhub.ai/jiafar/skills/amazon-scraper)
- [BSR Top 100 strategy](references/bsr-top100-strategy.md)
- [Reviews strategy](references/reviews-strategy.md)
- [CDP fallback strategy](references/cdp-fallback-strategy.md)

## Skill Output:

**Output Type(s):** [JSON data, Markdown guidance, Shell commands, Configuration instructions]

**Output Format:** [Structured JSON scrape results and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check the scrape status before relying on results; blocked pages may contain empty fields.]

## Skill Version(s):

4.0.1 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
