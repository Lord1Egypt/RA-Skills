## Description:

Build production-ready Bright Data integrations with best practices baked in. Reference documentation for developers using coding assistants (Claude Code, Cursor, etc.) to implement web scraping, search, browser automation, and structured data extraction. Covers Web Unlocker API, SERP API, Web Scraper API, and Browser API (Scraping Browser).

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and implement Bright Data Web Unlocker, SERP API, Web Scraper API, Browser API, and CLI patterns for web scraping, search, browser automation, and structured data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes remote or unpinned CLI execution patterns.

Mitigation: Prefer pinned, reviewable Bright Data CLI installation methods and review any curl-to-bash or unpinned npx command before running it.

Risk: Using the skill can share requested URLs or search inputs with Bright Data.

Mitigation: Use the skill only for data that is appropriate to send to Bright Data services and avoid sensitive, private, or regulated inputs unless approved.

Risk: Bright Data API keys and browser passwords can be exposed through prompts, logs, URLs, or repositories.

Mitigation: Keep credentials in environment variables or approved secret stores, avoid embedding them in URLs or source files, and redact them from logs and prompts.

## Reference(s):

- [Bright Data CLI Setup and Troubleshooting](artifact/references/cli-setup.md)
- [Web Unlocker API Reference](artifact/references/web-unlocker.md)
- [SERP API Reference](artifact/references/serp-api.md)
- [Web Scraper API Reference](artifact/references/web-scraper-api.md)
- [Browser API Reference](artifact/references/browser-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Python, JavaScript, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Bright Data account details, zones, API keys, browser credentials, target URLs, or search inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
