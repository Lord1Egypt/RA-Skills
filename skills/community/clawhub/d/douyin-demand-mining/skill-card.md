## Description:

Search public Douyin posts and creator accounts, retrieve trending topics and post details, and organize comment evidence into audience needs and pain point insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content researchers, creators, and marketers use this skill to find topics, monitor public creator accounts, and understand audience needs from Douyin posts and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied links are sent to a third-party data API.

Mitigation: Avoid sending sensitive queries or links, and get user approval before collecting the requested data.

Risk: The security scan only partially inspected 18 of 42 components, so its benign verdict does not cover all behavior.

Mitigation: Review the skill and rescan relevant changes before deployment, especially before using it with sensitive requests.

## Reference(s):

- [Comment demand analysis guide](references/demand-mining.md)
- [Command options](references/options.md)
- [Release changelog](references/changelog.md)
- [GUAIKEI service](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-demand-mining)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON records; concise Markdown analysis with comment evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public post, creator, comment, and trending data; comment analysis includes sample counts and verbatim supporting comments.]

## Skill Version(s):

1.4.2 (source: server-resolved release, frontmatter, changelog released 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
