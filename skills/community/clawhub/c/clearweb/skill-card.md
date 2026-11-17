## Description:

ClearWeb provides web search, webpage reading, screenshots, and structured data extraction for shell-capable agents through the Bright Data CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an agent needs public web search, page reading, screenshots, or structured extraction for research, monitoring, competitor analysis, lead generation, price checks, and documentation review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes web access and scraping through a third-party CLI and service.

Mitigation: Do not send sensitive URLs, private data, credentials, or confidential browsing targets through the service unless approved for that use.

Risk: The artifact includes curl-to-bash and elevated-permission installation guidance.

Mitigation: Use a reviewed and pinned installation path where possible, and avoid sudo-based global installs unless explicitly approved.

Risk: The skill supports CAPTCHA, bot-bypass, paywall, social-profile, and lead-generation workflows.

Mitigation: Confirm authorization, site terms, data rights, and applicable policy before using those workflows.

## Reference(s):

- [Web Search Reference](references/web-search.md)
- [Web Scraping Reference](references/web-scrape.md)
- [Structured Data Extraction Reference](references/data-extraction.md)
- [Troubleshooting Reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, Files]

**Output Format:** [Markdown guidance with bash commands; Bright Data CLI outputs may include markdown, JSON, CSV, NDJSON, HTML, or screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bright Data CLI setup and credentials for live web access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
