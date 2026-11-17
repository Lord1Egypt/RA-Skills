## Description:

Fetches public Bilibili content, including search results, creator video lists, video details, comments, and danmaku, using agent-browser and public APIs without requiring login for most data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[excalibursssooo](https://clawhub.ai/user/excalibursssooo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to collect Bilibili public video, creator, comment, and danmaku data and generate local JSON exports and Markdown harvest reports for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser state or cookie files may expose account-linked Bilibili data.

Mitigation: Use unauthenticated mode for public data when possible, keep any cookie file private, apply restrictive file permissions, and do not commit cookies to version control.

Risk: Harvested public and user-linked data is written locally, and shared temporary locations can expose data to other local users or jobs.

Mitigation: Set BI_DATA_DIR to a user-private directory before running harvest workflows and avoid relying on shared /tmp storage.

Risk: The skill may close all agent-browser sessions during SPA recovery, which can disrupt unrelated browser automation.

Mitigation: Run the skill in an isolated browser/session context and avoid concurrent agent-browser tasks during large harvests.

Risk: Optional danmaku features depend on unpinned Python packages.

Mitigation: Review and pin dependency versions in a controlled environment before enabling danmaku workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/excalibursssooo/skills/bilibili-universal)
- [Project homepage](https://github.com/excalibursssooo/bilibili-search)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Anti-scraping pitfalls and debugging notes](docs/pitfalls.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with shell commands plus generated JSON data files and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write harvested Bilibili data under the configured BI_DATA_DIR and can optionally use a private cookie file through BI_COOKIE_FILE.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
