## Description:

Web crawler using BFS and anti-scraping methods to extract BBC and general news content into structured Markdown with multi-site and deduplication support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixopt17](https://clawhub.ai/user/felixopt17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to crawl authorized news or website sources, extract article metadata and body text, and save the results as Markdown files with optional local image copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler fetches external pages and images and may encounter redirected or embedded URLs outside the apparent site boundary.

Mitigation: Run it in a constrained virtual environment or container, set explicit allowed domains, keep request delays conservative, and crawl only authorized targets.

Risk: Installation runs package installation commands and may install Playwright browser components.

Mitigation: Review dependency versions before installation, avoid privileged installs, and use a dedicated environment with limited filesystem and network access.

Risk: Collected web content may be copyrighted, sensitive, or governed by site-specific terms.

Mitigation: Respect robots.txt and site rules, confirm permission to crawl, and review saved outputs before reuse or redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felixopt17/skills/bbccrawlermaxclaw)
- [Artifact README](artifact/README.md)
- [Usage guide](artifact/USAGE.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files with YAML front matter, local image files, and plain-text failed URL logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crawler behavior is controlled by URL, output directory, page limit, depth, delay, method, and allowed-domain options.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
