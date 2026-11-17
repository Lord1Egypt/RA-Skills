## Description:

Performs deep web scraping using a Docker-based Crawlee and Playwright environment to extract validated, ad-free raw data from complex public sites like YouTube and X/Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run containerized browser scraping against public, authorized dynamic webpages and YouTube URLs, returning transcript, description, or page text as structured output for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary URL scraping can reach private, internal, authenticated, or otherwise unauthorized pages if the operator supplies unsafe targets.

Mitigation: Use the skill only for public pages you are authorized to scrape, block private and internal network ranges, and avoid authenticated content.

Risk: The browser workload runs in a weakly isolated Docker configuration and launches Chromium with sandbox-disabling flags.

Mitigation: Run it inside a strongly isolated container or VM, restrict outbound network access, mount code read-only, and review the runtime image before use.

Risk: Runtime npm dependencies and the browser image can change behavior or introduce vulnerabilities if left unreviewed.

Mitigation: Pin and review the runtime image and npm dependencies before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/abe-deep-scraper)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance]

**Output Format:** [JSON printed to stdout with status, type, source identifiers, and scraped text fields; Markdown guidance may include shell commands for Docker execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scraped transcript or page text is truncated by the handlers before output.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
