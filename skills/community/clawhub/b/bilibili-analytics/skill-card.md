## Description:

Bilibili Analytics searches Bilibili videos by keyword, scrapes public search result data, and generates statistical reports with video, author, playback, comment, and time-distribution summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcjinglang](https://clawhub.ai/user/pcjinglang)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agents use this skill to collect public Bilibili search results for a keyword, analyze video activity and engagement, and produce a Markdown report for trend or topic review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation to contact Bilibili and scrape public search result pages.

Mitigation: Use conservative page counts and delays, respect Bilibili access policies, and stop if pages show blocking or anti-automation responses.

Risk: Generated Markdown reports can include public web content such as titles and author names from scraped pages.

Mitigation: Review generated Markdown before sharing or rendering it in trusted contexts.

Risk: Global agent-browser installation or elevated install commands can broaden local execution risk.

Mitigation: Prefer a pinned, project-local agent-browser installation and do not run install commands with sudo or root privileges.

## Reference(s):

- [Bilibili Analytics skill page](https://clawhub.ai/pcjinglang/skills/bilibili-analytics)
- [Usage examples](references/usage-examples.md)
- [Bilibili search endpoint used by the skill](https://search.bilibili.com/all?keyword={keyword})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON data files, and shell/Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timestamped local JSON scrape files and Markdown reports from public Bilibili search result data.]

## Skill Version(s):

1.0.0 (source: server release metadata, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
