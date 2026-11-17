## Description:

Universal AI-powered web scraper for any platform. Scrape data from Instagram, Facebook, TikTok, YouTube, Google Maps, Google Search, Google Trends, Booking.com, and TripAdvisor. Use for lead generation, brand monitoring, competitor analysis, influencer discovery, trend research, content analytics, audience analysis, or any data extraction task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apify](https://clawhub.ai/user/apify)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to choose and run Apify Actors for public web data extraction, including lead generation, brand monitoring, competitor analysis, influencer discovery, trend research, content analytics, audience analysis, and review analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run broad public-data scraping workflows, including contact, email, follower, and audience datasets.

Mitigation: Use it only for lawful, consent-aware scraping goals and review platform terms, privacy obligations, and dataset scope before running an Actor.

Risk: Scraped output may include untrusted data, and CSV exports can carry downstream spreadsheet risks.

Mitigation: Prefer quick answers or JSON for untrusted data, and inspect CSV exports before opening or sharing them.

Risk: The skill requires an Apify token and sends Actor inputs to Apify services.

Mitigation: Install only when sharing the APIFY_TOKEN and task inputs with Apify is acceptable for the workspace.

Risk: Output files are written by user-selected filenames in the current project directory.

Mitigation: Use fresh, ordinary filenames without path separators or metacharacters, and avoid overwriting existing project files.

## Reference(s):

- [Apify Ultimate Scraper on ClawHub](https://clawhub.ai/apify/skills/apify-ultimate-scraper)
- [Apify Publisher Profile](https://clawhub.ai/user/apify)
- [Apify Homepage](https://apify.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus optional CSV or JSON scraper output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN, Node.js, and the mcpc CLI; exported files are written under the current working directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
