## Description:

Web scraping via SkillBoss API Hub for fetching full page content with JavaScript rendering, including complex pages with dynamic content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve rendered web page content and convert scrape results into clean markdown or JSON for downstream analysis, summarization, or documentation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs and scrape results are sent through SkillBoss API Hub using the user's SKILLBOSS_API_KEY.

Mitigation: Avoid private intranet pages, regulated data, and URLs containing tokens unless SkillBoss handling and retention terms are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-crawl-for-ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown or JSON returned from a command-line Node.js scraper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY; default output is clean markdown and --json returns the full JSON response.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
