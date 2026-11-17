## Description:

Searches Douyin public videos, posts, creator works, comments, and hot lists to support content research, competitor analysis, and trend discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content planners, analysts, and marketers use this skill to search public Douyin content and review creator, engagement, comment, and trend data for topic discovery, competitor research, and audience insight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and supplied Douyin links are sent to the third-party service at guaikei.com to retrieve results.

Mitigation: Use only public content and avoid submitting sensitive or unauthorized information; confirm the data-sharing scope is appropriate before querying.

Risk: The security scan reports benign findings with medium confidence, but 18 of 42 components were only partially inspected, including executable files.

Mitigation: Review the partially inspected components before installation, especially before running executable files.

## Reference(s):

- [Command options](references/options.md)
- [Comment demand research guide](references/demand-mining.md)
- [Release notes](references/changelog.md)
- [Official service and token setup](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-bluesea-collector)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data; concise text or Markdown summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover public Douyin content and may include engagement counts, creator details, comments, and links; the available fields depend on the selected command and service response.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
