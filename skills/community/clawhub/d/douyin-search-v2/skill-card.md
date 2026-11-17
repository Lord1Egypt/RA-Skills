## Description:

Collects Douyin search results and trending-search data with Playwright browser automation, natural-language keyword extraction, and JSON or CSV export.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content analysts use this skill to search Douyin by keyword or natural-language request, retrieve hot-list entries, and export structured video metadata for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation against Douyin may run with weakened browser isolation.

Mitigation: Run the skill in an isolated, non-root environment and remove sandbox-disabling launch flags where possible.

Risk: Mutable dependency and browser downloads can change the runtime behavior after installation.

Mitigation: Pin Playwright and browser versions, prefer trusted download sources, and verify any third-party mirrors before use.

Risk: Automated scraping can trigger captcha, rate limits, IP restrictions, or platform-rule issues.

Mitigation: Confirm each scraping request, keep limits and request frequency low, avoid logging into personal accounts, and follow Douyin platform rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-search-v2)
- [Playwright documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Console text with optional JSON or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include titles, descriptions, authors, engagement counts, URLs, tags, and publish dates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
