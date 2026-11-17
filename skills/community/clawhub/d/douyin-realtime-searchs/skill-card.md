## Description:

Searches current public Douyin videos and image posts, trending lists, creator posts, individual post details, and comments, returning structured results for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content planners, social media analysts, and account managers use it to find current Douyin content, monitor public creator activity, inspect post performance, and summarize comment sentiment or audience needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links are sent to the third-party Guaikei API.

Mitigation: Avoid sensitive inputs and confirm the data transfer and authorization scope before querying.

Risk: The security review is benign but medium confidence and partial; some executable files were only partly interpreted.

Mitigation: Review the remaining executable code before installation, or run the skill in a restricted environment.

## Reference(s):

- [Usage options](references/options.md)
- [Comment demand analysis guide](references/demand-mining.md)
- [Changelog](references/changelog.md)
- [Guaikei API service and help](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise Markdown summaries when analysis is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover public content and may include time-limited media or share links.]

## Skill Version(s):

1.4.2 (source: server-resolved release, SKILL.md frontmatter, changelog dated 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
