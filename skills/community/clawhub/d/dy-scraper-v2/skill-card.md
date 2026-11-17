## Description:

Searches Douyin videos and hot-list content from natural-language keywords, returning titles, links, descriptions, and engagement fields when available.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to answer Douyin video search or hot-list requests by extracting natural-language keywords, running the provided browser/search workflow, and presenting video metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation, external search fallback, and synthetic fallback data can produce unverified results while presenting the workflow as a scraper.

Mitigation: Run in an isolated, unprivileged environment; clearly distinguish real Douyin results, external search results, and synthetic examples; verify returned data before relying on it.

Risk: Automated access to Douyin may encounter anti-scraping controls, account safety issues, or platform-policy constraints.

Mitigation: Use conservative limits and delays, avoid logging into personal accounts, and confirm that collection complies with applicable law and Douyin platform rules.

Risk: Installation downloads browser automation dependencies and can use external search credentials when configured.

Mitigation: Review install scripts before execution, pin dependencies where possible, and avoid exposing unrelated environment secrets or API keys.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/dy-scraper-v2)
- [Playwright Documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown or terminal text summaries with optional JSON or CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and hot-list commands support keyword or category, result limit, output path, output format, headless mode, and delay options.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
