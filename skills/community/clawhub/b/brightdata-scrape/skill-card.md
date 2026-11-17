## Description:

Scrape helps agents fetch web content from one or more URLs as markdown, HTML, JSON, or screenshots through the Bright Data CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch raw or lightly structured web content from known URLs, URL lists, or paginated listings. It guides Bright Data CLI setup, output checks, block-page detection, and escalation when browser rendering or structured data feeds are more appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires authenticated Bright Data CLI access and may consume account resources when scraping pages or batches.

Mitigation: Verify CLI installation and authentication before use, review target URLs and batch size, and keep parallel scraping capped as shown in the artifact guidance.

Risk: Scraped output can be empty, blocked, or misleading if the target returns a CAPTCHA, Cloudflare page, or access-denied response.

Mitigation: Check output size, scan for block-page signatures, and confirm task-specific markers before treating a scrape as successful.

Risk: Legacy direct API fallback uses Bright Data credential environment variables and bypasses the preferred CLI path.

Mitigation: Use the fallback only when the CLI cannot be installed, review the command before execution, and avoid exposing API keys in logs or shared files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/meirk-brd/skills/brightdata-scrape)
- [bdata scrape flag reference](references/flags.md)
- [Scrape patterns](references/patterns.md)
- [Scrape worked examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or direct creation of markdown, HTML, JSON, and PNG screenshot files through Bright Data CLI commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
