## Description:

Scrape content from sites that block bots, including Twitter/X threads, Reddit, LinkedIn, YouTube comments, Google search results, and other sources, when standard web fetch is blocked and full thread or comment data is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research agents use this skill to run Apify actors for web scraping tasks when standard web fetch or search cannot retrieve complete content, such as full threads, comments, video metadata, and search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the release suspicious because the skill tells agents to run an unaudited local Apify runner script outside the package while using an Apify API key.

Mitigation: Install only when the local runner path is trusted or replace it with a bundled relative runner; use a limited Apify key with spending controls.

Risk: The skill sends scraping jobs and inputs to Apify infrastructure through the user's Apify account.

Mitigation: Avoid sending sensitive inputs unless the Apify account and actor configuration are approved for that data.

Risk: LinkedIn scraping is identified as terms-of-service sensitive in the artifact metadata.

Mitigation: Use LinkedIn scraping only for approved research workflows and confirm policy compliance before running the actor.

## Reference(s):

- [Apify Console](https://console.apify.com)
- [Apify Billing](https://console.apify.com/billing)
- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/apify-scraper)
- [Publisher Profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_API_KEY and python3; scraping runs through the user's Apify account and selected Apify actors.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
