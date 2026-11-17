## Description:

An AI-powered assistant for researching Douyin content through keyword search, creator post lookup, comments, post details, and trending topics, returning structured data for content and competitor analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, marketers, and analysts use this skill to search public Douyin posts, monitor creator accounts and trending topics, and examine comments for audience sentiment, content ideas, and competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided Douyin links and search terms to the GuaiKei service to retrieve results.

Mitigation: Review each query before execution and avoid sending confidential or identifying information.

Risk: Retrieved results are saved in the skill directory's logs folder and may contain research data.

Mitigation: Treat the logs as local research records and remove them when they are no longer needed.

Risk: ClawScan reports medium confidence because 18 of 42 components were only partially inspected, and it notes an undeclared single-post detail lookup.

Mitigation: Review the detail lookup behavior and the partially inspected code before installing or relying on the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/douyin-content-engineer)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Command options](artifact/references/options.md)
- [Change log](artifact/references/changelog.md)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise analysis or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include public post, creator, engagement, comment, and trend data.]

## Skill Version(s):

1.4.2 (source: server-resolved release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
