## Description:

Helps an agent interpret Chinese natural-language Douyin search or hot-list requests, run Playwright-based helper scripts, and return video metadata or exported result files.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content researchers use this skill to translate Chinese Douyin discovery requests into scraper commands and present or export example video metadata. It is appropriate for learning and research workflows where platform rules, request rates, and local execution risks are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises scraped Douyin trend data while the current search and hot-list implementations can return mock or fabricated example data.

Mitigation: Treat results as examples unless the implementation is independently verified against live Douyin pages.

Risk: Install scripts perform mutable dependency and browser installation.

Mitigation: Install and run the skill in an isolated, low-privilege environment with dependencies reviewed or pinned before deployment.

Risk: Output-file arguments can write broadly when supplied unsafe absolute or traversal paths.

Mitigation: Restrict output paths to an approved workspace directory and reject absolute or traversal paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-terry)
- [Playwright documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, files]

**Output Format:** [Text summaries with shell commands and optional JSON or CSV output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and hot-list commands accept keywords, categories, limits, output paths, and JSON or CSV format selection.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
