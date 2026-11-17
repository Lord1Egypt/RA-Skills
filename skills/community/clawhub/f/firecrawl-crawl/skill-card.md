## Description:

Bulk extract content from an entire website or site section by crawling pages under depth, path, page limit, delay, and concurrency controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect content from many pages on a website, such as a documentation section or bounded site area, and export crawl results for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows unpinned runtime execution of a third-party npm package through npx.

Mitigation: Use a preinstalled and reviewed Firecrawl binary or pin npx to an exact package version before running the skill.

Risk: Large or broad crawls can increase cost and collect more site data than intended.

Mitigation: Keep crawls scoped with include paths, maximum depth, page limits, delays, and concurrency controls.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/eohmig/skills/firecrawl-crawl)
- [Publisher Profile](https://clawhub.ai/user/eohmig)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and crawl option guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides Firecrawl crawl execution and JSON export paths; crawl scope and cost depend on user-selected limits.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
