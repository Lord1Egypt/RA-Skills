## Description:

抖音搜索爬虫 helps agents retrieve public Douyin search results, hot rankings, creator posts, video details, and comments for short-video research, competitor analysis, public-opinion monitoring, trend tracking, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and operators use this skill to collect structured public Douyin data for content research, competitor monitoring, public-opinion analysis, trend tracking, and marketing reports. The skill requires a GUAIKEI_API_TOKEN and supports keyword search, hot-list lookup, creator post retrieval, and comment retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin keywords, profile URLs, video URLs, and the GUAIKEI API token are sent to guaikei.com.

Mitigation: Use a low-privilege or revocable token, run the skill only where third-party API use is approved, and avoid running it on shared or CI machines.

Risk: Retrieved public Douyin result datasets are saved locally by default.

Mitigation: Review and delete the logs directory regularly, avoid collecting unnecessary personal data, and anonymize user-facing data before sharing.

Risk: Use of public platform data can involve platform terms, privacy, and redistribution constraints.

Mitigation: Confirm Douyin terms, authorization, and applicable privacy requirements before using results commercially or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-search-scraper-guaikei)
- [Source repository](https://github.com/why20261/douyin-search-scraper-guaikei)
- [Guaikei API service](https://www.guaikei.com)
- [Complete options](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output schemas](assets/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, files, guidance]

**Output Format:** [JSON on stdout, with logs on stderr and retrieved result datasets saved as local JSON files by default.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and a GUAIKEI_API_TOKEN environment variable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
