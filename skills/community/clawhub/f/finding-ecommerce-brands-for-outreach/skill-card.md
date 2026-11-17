## Description:

Discovers e-commerce and DTC brands on Instagram and TikTok using Apidojo's Apify scrapers, then filters and ranks accounts for outreach based on brand signals, follower counts, bios, product category, and engagement rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External B2B sales, wholesale, SaaS, and partnership teams use this skill to build prospect lists of e-commerce and DTC brands active on Instagram and TikTok. The agent prompts for category and platform constraints, scrapes candidate accounts, filters for brand signals, ranks results, and formats outreach-ready brand candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed if placed in URL query strings, shell history, logs, or traced commands.

Mitigation: Prefer MCP or authorization-header authentication, use a least-privileged Apify token, keep APIFY_TOKEN in the environment or an env file, and avoid shell tracing.

Risk: CSV or JSON exports may contain sensitive prospecting data collected from social platforms.

Mitigation: Treat exports as sensitive, limit access, and store or share only what the outreach workflow requires.

Risk: Scraping Instagram or TikTok for outreach can create compliance or platform-policy concerns.

Mitigation: Install and run only when comfortable using Apify to scrape those platforms, and review the workflow against applicable platform terms and outreach rules before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-ecommerce-brands-for-outreach)
- [Apidojo Instagram Scraper actor](https://apify.com/apidojo/instagram-scraper)
- [Apidojo TikTok Scraper actor](https://apify.com/apidojo/tiktok-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown table with highlights, notes, and optional CSV or JSON exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN and may use Apify MCP or REST API; results can be saved as CSV or JSON when helper scripts are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
