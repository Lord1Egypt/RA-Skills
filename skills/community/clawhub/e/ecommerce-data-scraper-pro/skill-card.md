## Description:

Extracts structured data from webpages and APIs, with batch processing and JSON, CSV, or Excel output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect public webpage or API data for ecommerce monitoring, market research, recruiting, real estate, social, or custom extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary internal or external URLs supplied by a user or agent.

Mitigation: Run it in a network-restricted sandbox, allow only intended HTTPS endpoints, and do not target private or internal services.

Risk: The API mode can send supplied bearer tokens or credentials to a configured endpoint.

Mitigation: Use scoped non-production credentials, avoid production tokens, and verify the endpoint before providing authentication material.

Risk: Scraping can create legal, privacy, or service-load exposure if aimed at inappropriate targets.

Mitigation: Use it only for public data where scraping is permitted, respect robots.txt and site terms, and keep request delays conservative.

Risk: Runtime output paths can write scraped data to local files.

Mitigation: Set explicit output paths and review generated files before using them in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chungvic/skills/ecommerce-data-scraper-pro)
- [Publisher profile](https://clawhub.ai/user/chungvic)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown guidance with CLI examples; scraper runtime output as JSON, CSV, or Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write output files to explicit user-selected paths and make outbound HTTP(S) requests to supplied URLs or API endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and artifact metadata list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
