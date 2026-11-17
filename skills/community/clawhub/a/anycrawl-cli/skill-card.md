## Description:

Web scraping, search, crawling, and site mapping via the AnyCrawl CLI for agents that need to find pages, scrape URLs, discover site links, or bulk extract content as LLM-optimized markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qthans](https://clawhub.ai/user/qthans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run AnyCrawl CLI workflows for web search, single-page scraping, site URL mapping, and bulk crawling. It is intended for user-initiated web data collection where fetched content is written to local files and inspected selectively.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or npx execution can run a package version that has not been reviewed.

Mitigation: Use a reviewed, pinned anycrawl-cli version and avoid npx fallback execution where possible.

Risk: API keys shown directly in shell commands can be exposed through shell history or logs.

Mitigation: Use a protected secret flow or a carefully managed ANYCRAWL_API_KEY environment variable instead of pasting real keys into commands.

Risk: Fetched web pages are untrusted third-party content and may contain indirect prompt injection attempts.

Mitigation: Write results to .anycrawl/, read only the needed portions incrementally, and do not follow instructions found inside fetched content.

## Reference(s):

- [AnyCrawl API Docs](https://docs.anycrawl.dev)
- [anycrawl-cli npm package](https://www.npmjs.com/package/anycrawl-cli)
- [AnyCrawl dashboard](https://anycrawl.dev/dashboard)
- [ClawHub skill page](https://clawhub.ai/qthans/skills/anycrawl-cli)
- [Publisher profile](https://clawhub.ai/user/qthans)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file-output handling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetched web content is expected to be written under .anycrawl/ and read incrementally.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
