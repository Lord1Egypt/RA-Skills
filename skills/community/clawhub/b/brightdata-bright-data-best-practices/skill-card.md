## Description: <br>
Build production-ready Bright Data integrations with best practices baked in. Reference documentation for developers using coding assistants (Claude Code, Cursor, etc.) to implement web scraping, search, browser automation, and structured data extraction. Covers Web Unlocker API, SERP API, Web Scraper API, and Browser API (Scraping Browser). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and implement the right Bright Data API or CLI workflow for web scraping, search extraction, browser automation, and structured data extraction tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bright Data API keys, Browser API passwords, session cookies, and request headers can expose sensitive access if copied into chats, logs, or repositories. <br>
Mitigation: Use environment variables or the Bright Data CLI credential store, redact secrets from agent transcripts and logs, and avoid forwarding production cookies or sensitive headers. <br>
Risk: Installer commands and one-off CLI execution can run downloaded code on the user's machine. <br>
Mitigation: Prefer npm or npx for Bright Data CLI use, inspect downloaded installers before running them, and install only when Bright Data services are intended. <br>
Risk: Scraping workflows can create billing, legal, terms-of-service, or data-handling exposure. <br>
Mitigation: Confirm approval for target sites and data categories, avoid internal or regulated data without authorization, and monitor Bright Data usage and billing. <br>


## Reference(s): <br>
- [Bright Data CLI Setup and Troubleshooting](references/cli-setup.md) <br>
- [Web Unlocker API Reference](references/web-unlocker.md) <br>
- [SERP API Reference](references/serp-api.md) <br>
- [Web Scraper API Reference](references/web-scraper-api.md) <br>
- [Browser API (Scraping Browser) Reference](references/browser-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; may include credential placeholders and command snippets for the agent to adapt.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
