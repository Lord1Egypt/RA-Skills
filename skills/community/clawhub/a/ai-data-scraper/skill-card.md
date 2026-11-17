## Description:

Automates web and API data extraction with cleaning, formatting, scheduling, proxy support, retries, deduplication, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthasking123](https://clawhub.ai/user/arthasking123)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to collect and format data from authorized web pages and APIs, including recurring scraping workflows and saved outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated URL inputs can reach local files or internal services and save the results.

Mitigation: Use only URLs the user is authorized to access, avoid sensitive or internal targets, and add HTTPS-only validation, private-network blocking, redirect controls, allowlists, and rate limits before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arthasking123/skills/ai-data-scraper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash examples and generated JSON, HTML, or text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes fetched content under ./output with timestamped filenames when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
