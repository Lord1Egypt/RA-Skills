## Description:

Scrape complete business intelligence from Google Maps, Facebook, and Instagram for any local business. Returns structured JSON with ratings, contact info, services, and media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamsarts](https://clawhub.ai/user/dreamsarts)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, growth teams, and lead-generation operators use this skill to collect structured local-business profiles for Ghost Closer page building, prospect research, and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scraper connects to an existing Chrome session, which can expose logged-in browser state.

Mitigation: Run it only against an isolated browser profile with no personal logins or sensitive sessions.

Risk: The scraper loads a hard-coded .env path, which can unnecessarily expose local secrets.

Mitigation: Remove the hard-coded environment loading and provide only the minimum required configuration through a reviewed path.

Risk: The scraper follows public web pages and business-site URLs, which can create redirect and sensitive-network exposure.

Mitigation: Validate target URLs and redirects before scraping, and avoid use on sensitive networks.

Risk: Scraping Google Maps, Facebook, Instagram, and business websites can raise terms-of-service and data-handling obligations.

Mitigation: Confirm the operator is allowed to scrape the target services and handle collected business/profile data appropriately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamsarts/skills/ghost-closer-web-scraper)
- [Publisher profile](https://clawhub.ai/user/dreamsarts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; scraper output is structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scraper returns nullable sections for unavailable sources and logs errors to stderr while preserving JSON on stdout.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
