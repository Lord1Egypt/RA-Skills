## Description:

Retrieves Douyin hot-search data and keyword search results, including natural-language search requests.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Douyin hot-search topics or keyword-related video metadata and optionally save results for review or downstream analysis. The artifact describes the data use as learning and research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser mode launches Chromium with an unsafe configuration.

Mitigation: Prefer API-only mode where possible, run browser mode only in an isolated environment, and avoid privileged execution.

Risk: Install steps pull unpinned Playwright and Chromium dependencies.

Mitigation: Pin and verify Playwright and Chromium versions before installation.

Risk: Scraping behavior can be invoked for broad Douyin search requests.

Mitigation: Require explicit Douyin-specific user intent and review platform rules before running the scraper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-hot-scraper)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)
- [Douyin hot-search API endpoint](https://www.douyin.com/aweme/v1/web/hot/search/list/)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Console text with optional JSON or CSV file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include video or hot-search fields such as title, author, engagement counts, URL, tags, publish date, hot value, and search word.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
