## Description:

Crawlee Web Scraper helps agents fetch single or bulk URLs with Crawlee-backed retries and fallback handling when ordinary HTTP requests are blocked by rate limits or bot detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryantegomoh](https://clawhub.ai/user/bryantegomoh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scrape authorized web pages when ordinary HTTP fetching is blocked, including single URL lookups and bulk URL collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for bot-detection evasion and bulk fetching, which can be misused against sites where scraping is not authorized.

Mitigation: Use it only for sites you are authorized to access, and review site terms, robots guidance, and applicable rate limits before running bulk jobs.

Risk: Untrusted URL lists can cause requests to internal services or cloud metadata endpoints from a privileged environment.

Mitigation: Run the scraper in an isolated, least-privileged environment with outbound network restrictions and reject untrusted URL lists.

Risk: Runtime dependency changes can alter crawling behavior or security posture.

Mitigation: Pin the Crawlee and requests dependencies and review updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bryantegomoh/skills/crawlee-web-scraper)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python and shell examples; scraper output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text extraction is capped at 10000 characters per URL and HTML preview output is capped at 2000 characters per URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
