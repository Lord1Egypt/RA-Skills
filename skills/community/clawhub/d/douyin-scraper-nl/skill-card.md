## Description:

Douyin Scraper helps agents turn Chinese natural-language Douyin search or hot-list requests into Playwright-backed scraping commands that return terminal summaries and JSON or CSV result files.

This skill is for research and development only.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route Chinese natural-language requests into Douyin keyword searches or hot-list lookups, then inspect or save the resulting video metadata. It is most appropriate for research and content discovery workflows where platform rules, request rate, account exposure, and mock-result labeling are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs browser automation tooling.

Mitigation: Review and pin dependencies before installation, and run the skill in an isolated environment with only the workspace access it needs.

Risk: Live Douyin requests may trigger platform, account, IP, or compliance issues.

Mitigation: Follow Douyin platform rules, keep request rates low, avoid sensitive credentials or broad workspace mounts, and review whether login or proxy use is appropriate.

Risk: Some outputs may be mock or demo data rather than live scrape results.

Mitigation: Check the mock=true field and independently verify records before using them for decisions or downstream publication.

Risk: The Node path and broad natural-language triggers may produce less reliable or unintended behavior.

Mitigation: Prefer the Python nl, search, and hot commands for normal use, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/douyin-scraper-nl)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)
- [Playwright documentation](https://playwright.dev/)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands; scraper output as terminal text plus JSON or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain mock=true records when Playwright is unavailable, live extraction fails, or Douyin access is blocked.]

## Skill Version(s):

3.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
